import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.services.encryption import decrypt, encrypt


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    github_login: Mapped[str] = mapped_column(String(255), nullable=False)
    _github_access_token: Mapped[str] = mapped_column(
        "github_access_token", Text, nullable=False
    )
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (Index("idx_users_github_id", "github_id"),)

    @property
    def github_access_token(self) -> str:
        value = self._github_access_token
        if not value:
            return ""
        try:
            return decrypt(value)
        except Exception:
            # Unencrypted legacy token — return as-is
            return value

    @github_access_token.setter
    def github_access_token(self, value: str) -> None:
        self._github_access_token = encrypt(value) if value else ""
