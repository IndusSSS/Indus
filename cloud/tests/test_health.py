# tests/test_health.py
"""
Health check tests.

Basic functionality tests for the application.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_import():
    """Test that the app can be imported successfully."""
    assert app is not None
    assert hasattr(app, "routes")


if __name__ == "__main__":
    pytest.main([__file__])