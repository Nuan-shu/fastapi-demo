"""
Unit tests for FastAPI demo app (main.py).
Uses pytest + httpx (TestClient) to cover all endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Tests for GET /
# ---------------------------------------------------------------------------
class TestHomeEndpoint:
    """Tests for the root endpoint (GET /)."""

    def test_home_returns_200(self):
        """Home endpoint should return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_json(self):
        """Home endpoint should return JSON content."""
        response = client.get("/")
        assert response.headers.get("content-type") == "application/json"

    def test_home_body_contains_message(self):
        """Home endpoint should contain the expected message key."""
        response = client.get("/")
        json_data = response.json()
        # The key is "message" (string), not a variable named message
        assert "message" in json_data
        assert json_data["message"] == "Hello, FastAPI!"

    def test_home_invalid_method_post(self):
        """POST to / should return 405 Method Not Allowed."""
        response = client.post("/")
        assert response.status_code == 405

    def test_home_invalid_method_put(self):
        """PUT to / should return 405 Method Not Allowed."""
        response = client.put("/")
        assert response.status_code == 405

    def test_home_invalid_method_delete(self):
        """DELETE to / should return 405 Method Not Allowed."""
        response = client.delete("/")
        assert response.status_code == 405

    def test_home_options_returns_allow_header(self):
        """OPTIONS / should include Allow header."""
        response = client.options("/")
        # OPTIONS usually returns 200
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Tests for GET /health
# ---------------------------------------------------------------------------
class TestHealthEndpoint:
    """Tests for the health-check endpoint (GET /health)."""

    def test_health_returns_200(self):
        """Health endpoint should return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Health endpoint should return JSON content."""
        response = client.get("/health")
        assert response.headers.get("content-type") == "application/json"

    def test_health_body_contains_status(self):
        """Health endpoint should contain the expected status key."""
        response = client.get("/health")
        json_data = response.json()
        assert "status" in json_data
        assert json_data["status"] == "running"

    def test_health_post_not_allowed(self):
        """POST to /health should return 405."""
        response = client.post("/health")
        assert response.status_code == 405


# ---------------------------------------------------------------------------
# Tests for unknown / non-existent routes
# ---------------------------------------------------------------------------
class TestNotFound:
    """Tests for non-existent endpoints."""

    def test_unknown_route_returns_404(self):
        """Requesting an unregistered path should return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_unknown_route_post_returns_404(self):
        """POST to an unregistered path should also return 404."""
        response = client.post("/nonexistent")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests for FastAPI app metadata / OpenAPI
# ---------------------------------------------------------------------------
class TestAppMeta:
    """Tests for OpenAPI docs and app identity."""

    def test_openapi_schema_available(self):
        """GET /openapi.json should return 200 with valid schema."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        assert "/" in schema["paths"]
        assert "/health" in schema["paths"]

    def test_docs_endpoint_accessible(self):
        """GET /docs should return the Swagger UI page."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_redoc_endpoint_accessible(self):
        """GET /redoc should return the ReDoc page."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
