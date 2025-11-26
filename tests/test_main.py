"""
Tests for main application endpoints.
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


class TestIndexEndpoint:
    """Tests for the root endpoint."""

    def test_index_returns_200(self, client):
        """Test that index returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_json(self, client):
        """Test that index returns JSON response."""
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_index_contains_message(self, client):
        """Test that index contains welcome message."""
        response = client.get("/")
        data = response.get_json()
        assert "message" in data
        assert "Welcome" in data["message"]

    def test_index_contains_version(self, client):
        """Test that index contains version information."""
        response = client.get("/")
        data = response.get_json()
        assert "version" in data

    def test_index_contains_environment(self, client):
        """Test that index contains environment information."""
        response = client.get("/")
        data = response.get_json()
        assert "environment" in data


class TestVersionEndpoint:
    """Tests for the version endpoint."""

    def test_version_returns_200(self, client):
        """Test that version endpoint returns 200."""
        response = client.get("/api/version")
        assert response.status_code == 200

    def test_version_contains_version(self, client):
        """Test that version endpoint contains version."""
        response = client.get("/api/version")
        data = response.get_json()
        assert "version" in data

    def test_version_contains_environment(self, client):
        """Test that version endpoint contains environment."""
        response = client.get("/api/version")
        data = response.get_json()
        assert "environment" in data


class TestInfoEndpoint:
    """Tests for the info endpoint."""

    def test_info_returns_200(self, client):
        """Test that info endpoint returns 200."""
        response = client.get("/api/info")
        assert response.status_code == 200

    def test_info_contains_name(self, client):
        """Test that info endpoint contains application name."""
        response = client.get("/api/info")
        data = response.get_json()
        assert "name" in data

    def test_info_contains_endpoints(self, client):
        """Test that info endpoint lists available endpoints."""
        response = client.get("/api/info")
        data = response.get_json()
        assert "endpoints" in data
        assert isinstance(data["endpoints"], list)
        assert len(data["endpoints"]) > 0
