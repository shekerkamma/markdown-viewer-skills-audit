import logging

import httpx

logger = logging.getLogger(__name__)


async def notify_escalation(
    webhook_url: str,
    repo_full_name: str,
    issue_number: int,
    agent_name: str,
    reason: str,
) -> None:
    if not webhook_url:
        return

    message = {
        "text": f":warning: *TicketForge Escalation* — `{repo_full_name}#{issue_number}`",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f":warning: *TicketForge Escalation*\n\n"
                        f"*Repo:* `{repo_full_name}`\n"
                        f"*Issue:* #{issue_number}\n"
                        f"*Agent:* {agent_name}\n"
                        f"*Reason:* {reason}"
                    ),
                },
            },
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(webhook_url, json=message, timeout=10)
            resp.raise_for_status()
    except Exception as e:
        logger.warning("Failed to send Slack notification: %s", e)
