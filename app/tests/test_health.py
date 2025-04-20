"""Tests for application health check endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Validates that the /health endpoint returns status 200."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
