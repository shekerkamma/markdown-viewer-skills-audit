import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import get_session
from app.models.team import Team, TeamMember
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])


class CreateTeamRequest(BaseModel):
    name: str


@router.get("")
async def list_teams(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Team, TeamMember.role)
        .join(TeamMember, TeamMember.team_id == Team.id)
        .where(TeamMember.user_id == user.id)
    )
    teams = []
    for team, role in result.all():
        count_result = await session.execute(
            select(func.count()).select_from(TeamMember).where(TeamMember.team_id == team.id)
        )
        member_count = count_result.scalar()
        teams.append({
            "id": str(team.id),
            "name": team.name,
            "plan": team.plan,
            "role": role,
            "member_count": member_count,
        })
    return {"teams": teams}


@router.post("", status_code=201)
async def create_team(
    body: CreateTeamRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    team = Team(name=body.name, owner_id=user.id)
    session.add(team)
    await session.flush()

    member = TeamMember(team_id=team.id, user_id=user.id, role="owner")
    session.add(member)
    await session.commit()
    await session.refresh(team)

    return {"id": str(team.id), "name": team.name, "plan": team.plan, "owner_id": str(team.owner_id)}


@router.get("/{team_id}")
async def get_team(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Verify membership
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    result = await session.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()
    if not team:
        raise HTTPException(404, detail="Team not found")

    # Get members
    result = await session.execute(
        select(User.github_login, User.avatar_url, TeamMember.role)
        .join(TeamMember, TeamMember.user_id == User.id)
        .where(TeamMember.team_id == team_id)
    )
    members = [
        {"github_login": login, "avatar_url": avatar, "role": role}
        for login, avatar, role in result.all()
    ]

    # Get repos
    from app.models.repository import Repository

    result = await session.execute(
        select(Repository).where(Repository.team_id == team_id)
    )
    repos = [
        {
            "id": str(r.id),
            "full_name": r.full_name,
            "is_active": r.is_active,
            "trigger_labels": r.trigger_labels,
        }
        for r in result.scalars().all()
    ]

    return {
        "id": str(team.id),
        "name": team.name,
        "plan": team.plan,
        "owner_id": str(team.owner_id),
        "members": members,
        "repositories": repos,
    }
