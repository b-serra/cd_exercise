"""
Tests for health check endpoints.
"""

import pytest
from src.app.main import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestHealthEndpoint:
    """Tests for the general health endpoint."""

    def test_health_returns_200(self, client):
        """Test that health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Test that health endpoint returns JSON."""
        response = client.get("/health")
        assert response.content_type == "application/json"

    def test_health_status_is_healthy(self, client):
        """Test that health status is healthy."""
        response = client.get("/health")
        data = response.get_json()
        assert data["status"] == "healthy"

    def test_health_contains_uptime(self, client):
        """Test that health response contains uptime."""
        response = client.get("/health")
        data = response.get_json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))

    def test_health_trailing_slash(self, client):
        """Test that health endpoint works with trailing slash."""
        response = client.get("/health/")
        assert response.status_code == 200


class TestReadinessEndpoint:
    """Tests for the readiness probe endpoint."""

    def test_readiness_returns_200(self, client):
        """Test that readiness endpoint returns 200."""
        response = client.get("/health/ready")
        assert response.status_code == 200

    def test_readiness_status_is_ready(self, client):
        """Test that readiness status is ready."""
        response = client.get("/health/ready")
        data = response.get_json()
        assert data["status"] == "ready"

    def test_readiness_contains_checks(self, client):
        """Test that readiness response contains checks."""
        response = client.get("/health/ready")
        data = response.get_json()
        assert "checks" in data
        assert isinstance(data["checks"], dict)

    def test_readiness_checks_database(self, client):
        """Test that readiness checks database."""
        response = client.get("/health/ready")
        data = response.get_json()
        assert "database" in data["checks"]

    def test_readiness_checks_cache(self, client):
        """Test that readiness checks cache."""
        response = client.get("/health/ready")
        data = response.get_json()
        assert "cache" in data["checks"]


class TestLivenessEndpoint:
    """Tests for the liveness probe endpoint."""

    def test_liveness_returns_200(self, client):
        """Test that liveness endpoint returns 200."""
        response = client.get("/health/live")
        assert response.status_code == 200

    def test_liveness_status_is_alive(self, client):
        """Test that liveness status is alive."""
        response = client.get("/health/live")
        data = response.get_json()
        assert data["status"] == "alive"

    def test_liveness_contains_timestamp(self, client):
        """Test that liveness response contains timestamp."""
        response = client.get("/health/live")
        data = response.get_json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], (int, float))
