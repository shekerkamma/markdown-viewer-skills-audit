import asyncio
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def mock_docker_client():
    client = MagicMock()
    container = MagicMock()
    container.id = "abc123def456"
    container.exec_run.return_value = (0, (b"output", b""))
    container.stop = MagicMock()
    container.remove = MagicMock()
    client.containers.run.return_value = container
    client.containers.get.return_value = container
    return client
