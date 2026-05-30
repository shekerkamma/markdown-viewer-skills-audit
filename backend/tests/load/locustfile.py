"""
Load test scenarios for TicketForge.

Usage:
    pip install locust
    locust -f backend/tests/load/locustfile.py --host http://localhost:8000

Scenarios:
1. Webhook delivery (100 concurrent)
2. Dashboard API (50 concurrent users)
3. Health check baseline
"""

import json
import hashlib
import hmac
import uuid

from locust import HttpUser, between, task


WEBHOOK_SECRET = "test-webhook-secret"


def sign_payload(payload: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


class WebhookUser(HttpUser):
    """Simulates GitHub sending webhook events."""

    wait_time = between(0.1, 0.5)

    @task
    def send_webhook(self):
        issue_number = uuid.uuid4().int % 100000
        payload = json.dumps({
            "action": "opened",
            "issue": {
                "number": issue_number,
                "html_url": f"https://github.com/test/repo/issues/{issue_number}",
                "title": f"Load test issue {issue_number}",
                "body": "Load test body",
                "labels": [{"name": "bug"}],
            },
            "repository": {
                "id": 12345,
                "full_name": "test/repo",
            },
        }).encode()

        self.client.post(
            "/api/webhooks/github",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": sign_payload(payload, WEBHOOK_SECRET),
                "X-GitHub-Event": "issues",
            },
        )


class DashboardUser(HttpUser):
    """Simulates authenticated dashboard users."""

    wait_time = between(1, 3)

    def on_start(self):
        # Use a test JWT token — in a real test, generate one against the test DB
        self.token = "test-jwt-token"
        self.team_id = str(uuid.uuid4())

    @task(3)
    def view_dashboard(self):
        self.client.get(
            "/api/v1/teams",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/v1/teams",
        )

    @task(2)
    def view_tickets(self):
        self.client.get(
            f"/api/v1/teams/{self.team_id}/tickets?limit=20",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/v1/teams/:id/tickets",
        )

    @task(1)
    def view_analytics(self):
        self.client.get(
            f"/api/v1/teams/{self.team_id}/analytics?period=30d",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/v1/teams/:id/analytics",
        )

    @task(5)
    def health_check(self):
        self.client.get("/api/health")
