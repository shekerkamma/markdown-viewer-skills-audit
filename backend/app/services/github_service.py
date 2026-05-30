import hashlib
import hmac
import logging

import httpx

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"


class GitHubService:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=GITHUB_API,
            headers={"Accept": "application/vnd.github+json"},
            timeout=30.0,
        )

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        expected = "sha256=" + hmac.new(
            secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    async def get_issue(self, repo: str, number: int, token: str) -> dict:
        response = await self._client.get(
            f"/repos/{repo}/issues/{number}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()

    async def create_pr(
        self, repo: str, branch: str, title: str, body: str, token: str
    ) -> dict:
        response = await self._client.post(
            f"/repos/{repo}/pulls",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": title,
                "body": body,
                "head": branch,
                "base": "main",
            },
        )
        response.raise_for_status()
        return response.json()

    async def post_comment(
        self, repo: str, issue_number: int, comment: str, token: str
    ) -> None:
        response = await self._client.post(
            f"/repos/{repo}/issues/{issue_number}/comments",
            headers={"Authorization": f"Bearer {token}"},
            json={"body": comment},
        )
        response.raise_for_status()

    async def register_webhook(
        self, repo: str, url: str, secret: str, token: str
    ) -> int:
        response = await self._client.post(
            f"/repos/{repo}/hooks",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "web",
                "active": True,
                "events": ["issues", "pull_request"],
                "config": {
                    "url": url,
                    "content_type": "json",
                    "secret": secret,
                    "insecure_ssl": "0",
                },
            },
        )
        response.raise_for_status()
        return response.json()["id"]

    async def close(self) -> None:
        await self._client.aclose()
