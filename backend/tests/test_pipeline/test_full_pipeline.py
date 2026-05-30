import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.base import AgentResult
from app.agents.code_reviewer import CodeReviewerAgent
from app.agents.content_researcher import ContentResearcherAgent


class TestContentResearcherAgent:
    @pytest.mark.asyncio
    async def test_successful_analysis(self):
        mock_logger = AsyncMock()
        mock_logger.log = AsyncMock()

        mock_claude = MagicMock()
        mock_claude.analyze = AsyncMock(return_value=json.dumps({
            "problem_statement": "NullPointerError in billing handler",
            "affected_files": ["billing.py"],
            "reproduction_steps": ["Process a payment", "Error at line 47"],
            "severity": "high",
            "confidence": 0.85,
        }))
        mock_claude.total_tokens_used = 500

        import uuid
        agent = ContentResearcherAgent(uuid.uuid4(), mock_logger, mock_claude)
        result = await agent.run({
            "title": "NullPointerError in billing handler",
            "body": "When processing a payment, a NullPointerError is thrown at line 47.",
            "labels": ["bug"],
            "issue_number": 42,
        })

        assert result.success is True
        assert result.confidence == 0.85
        assert result.output["severity"] == "high"

    @pytest.mark.asyncio
    async def test_low_confidence_escalation(self):
        mock_logger = AsyncMock()
        mock_logger.log = AsyncMock()

        mock_claude = MagicMock()
        mock_claude.analyze = AsyncMock(return_value=json.dumps({
            "problem_statement": "Something is broken",
            "affected_files": [],
            "reproduction_steps": [],
            "severity": "low",
            "confidence": 0.2,
        }))
        mock_claude.total_tokens_used = 300

        import uuid
        agent = ContentResearcherAgent(uuid.uuid4(), mock_logger, mock_claude)
        result = await agent.run({
            "title": "Bug",
            "body": "",
            "labels": ["bug"],
            "issue_number": 99,
        })

        assert result.success is False
        assert result.confidence == 0.2
        assert "Low confidence" in result.error


class TestCodeReviewerAgent:
    @pytest.mark.asyncio
    async def test_approve_clean_fix(self):
        mock_logger = AsyncMock()
        mock_logger.log = AsyncMock()

        mock_claude = MagicMock()
        mock_claude.analyze = AsyncMock(return_value=json.dumps({
            "overall": "approve",
            "dimensions": {
                "style": {"score": 0.9, "notes": "Consistent with codebase"},
                "tests": {"score": 0.8, "notes": "Test added"},
                "regression": {"score": 0.9, "notes": "Low risk"},
                "security": {"score": 1.0, "notes": "No issues"},
            },
            "confidence": 0.85,
            "summary": "Clean fix with good test coverage",
        }))
        mock_claude.total_tokens_used = 400

        import uuid
        agent = CodeReviewerAgent(uuid.uuid4(), mock_logger, mock_claude)
        result = await agent.run({
            "diff": "--- a/billing.py\n+++ b/billing.py\n@@ -45,3 +45,5 @@\n+if payment is None:\n+    raise ValueError('Payment cannot be None')",
            "analysis": {"problem_statement": "NullPointerError", "affected_files": ["billing.py"]},
        })

        assert result.success is True
        assert result.confidence == 0.85

    @pytest.mark.asyncio
    async def test_reject_security_issue(self):
        mock_logger = AsyncMock()
        mock_logger.log = AsyncMock()

        mock_claude = MagicMock()
        mock_claude.analyze = AsyncMock(return_value=json.dumps({
            "overall": "approve",
            "dimensions": {
                "style": {"score": 0.8, "notes": "OK"},
                "tests": {"score": 0.7, "notes": "Basic test"},
                "regression": {"score": 0.7, "notes": "Low risk"},
                "security": {"score": 0.2, "notes": "Hardcoded API key detected"},
            },
            "confidence": 0.7,
            "summary": "Fix contains hardcoded API key",
        }))
        mock_claude.total_tokens_used = 350

        import uuid
        agent = CodeReviewerAgent(uuid.uuid4(), mock_logger, mock_claude)
        result = await agent.run({
            "diff": "--- a/config.py\n+++ b/config.py\n@@ -1 +1 @@\n+API_KEY = 'sk-12345'",
            "analysis": {"problem_statement": "Config issue"},
        })

        assert result.success is False
        assert "rejected" in result.error.lower() or "security" in result.error.lower()

    @pytest.mark.asyncio
    async def test_escalate_uncertain_confidence(self):
        mock_logger = AsyncMock()
        mock_logger.log = AsyncMock()

        mock_claude = MagicMock()
        mock_claude.analyze = AsyncMock(return_value=json.dumps({
            "overall": "approve",
            "dimensions": {
                "style": {"score": 0.5, "notes": "Uncertain"},
                "tests": {"score": 0.4, "notes": "Missing tests"},
                "regression": {"score": 0.5, "notes": "Moderate risk"},
                "security": {"score": 0.8, "notes": "OK"},
            },
            "confidence": 0.5,
            "summary": "Uncertain about fix quality",
        }))
        mock_claude.total_tokens_used = 300

        import uuid
        agent = CodeReviewerAgent(uuid.uuid4(), mock_logger, mock_claude)
        result = await agent.run({
            "diff": "--- a/handler.py\n+++ b/handler.py\n@@ -10 +10 @@\n+pass",
            "analysis": {"problem_statement": "Handler issue"},
        })

        assert result.success is False
        assert "uncertain" in result.error.lower() or "escalat" in result.error.lower()
