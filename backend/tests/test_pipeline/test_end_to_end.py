import hashlib
import hmac
import json
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def make_webhook_payload(
    action: str = "opened",
    issue_number: int = 42,
    repo_id: int = 12345,
    labels: list[dict] | None = None,
):
    if labels is None:
        labels = [{"name": "bug"}]
    return {
        "action": action,
        "issue": {
            "number": issue_number,
            "title": "NullPointerError in billing handler",
            "body": "When processing a payment, a NullPointerError is thrown at line 47 of billing.py.",
            "html_url": f"https://github.com/org/repo/issues/{issue_number}",
            "labels": labels,
        },
        "repository": {
            "id": repo_id,
            "full_name": "org/repo",
        },
    }


def sign_payload(payload: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


class TestWebhookEndpoint:
    def setup_method(self):
        self.client = TestClient(app)

    def test_invalid_signature_returns_401(self):
        payload = json.dumps(make_webhook_payload()).encode()
        response = self.client.post(
            "/api/webhooks/github",
            content=payload,
            headers={
                "X-Hub-Signature-256": "sha256=invalid",
                "X-GitHub-Event": "issues",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 401

    def test_non_issue_event_is_ignored(self):
        payload = json.dumps({"action": "pushed"}).encode()
        sig = sign_payload(payload, settings.github_webhook_secret)
        response = self.client.post(
            "/api/webhooks/github",
            content=payload,
            headers={
                "X-Hub-Signature-256": sig,
                "X-GitHub-Event": "push",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 200
        assert response.json()["action"] == "ignored"

    def test_unhandled_action_is_ignored(self):
        data = make_webhook_payload(action="closed")
        payload = json.dumps(data).encode()
        sig = sign_payload(payload, settings.github_webhook_secret)
        response = self.client.post(
            "/api/webhooks/github",
            content=payload,
            headers={
                "X-Hub-Signature-256": sig,
                "X-GitHub-Event": "issues",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 200
        assert response.json()["action"] == "ignored"

    @patch("app.api.webhooks.async_session_factory")
    def test_unregistered_repo_is_ignored(self, mock_session_factory):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_session_factory.return_value = mock_session

        data = make_webhook_payload()
        payload = json.dumps(data).encode()
        sig = sign_payload(payload, settings.github_webhook_secret)
        response = self.client.post(
            "/api/webhooks/github",
            content=payload,
            headers={
                "X-Hub-Signature-256": sig,
                "X-GitHub-Event": "issues",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 200
        assert response.json()["reason"] == "repo not registered"
