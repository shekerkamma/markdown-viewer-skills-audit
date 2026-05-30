from unittest.mock import MagicMock, patch

import pytest

from app.services.docker_service import DockerService


@pytest.fixture
def docker_service(mock_docker_client):
    service = DockerService.__new__(DockerService)
    service.client = mock_docker_client
    return service


@pytest.mark.asyncio
async def test_create_sandbox(docker_service, mock_docker_client):
    container_id = await docker_service.create_sandbox("https://github.com/org/repo", "main")
    assert container_id == "abc123def456"
    mock_docker_client.containers.run.assert_called_once()
    call_kwargs = mock_docker_client.containers.run.call_args
    assert call_kwargs.kwargs["network_mode"] == "none"
    assert call_kwargs.kwargs["mem_limit"] == "2g"


@pytest.mark.asyncio
async def test_exec_in_sandbox(docker_service, mock_docker_client):
    output = await docker_service.exec_in_sandbox("abc123def456", "echo hello")
    assert "output" in output
    mock_docker_client.containers.get.assert_called_once_with("abc123def456")


@pytest.mark.asyncio
async def test_destroy_sandbox(docker_service, mock_docker_client):
    await docker_service.destroy_sandbox("abc123def456")
    container = mock_docker_client.containers.get.return_value
    container.stop.assert_called_once()
    container.remove.assert_called_once_with(force=True)
