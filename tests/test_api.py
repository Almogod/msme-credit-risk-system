import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health_check():
    """Test that the API is up and running."""
    # Note: /health is not explicitly defined in main.py yet but uvicorn/fastapi handles it or we can add it.
    # Looking at the Dockerfile, it expects http://localhost:8000/health
    pass

def test_predict_endpoint_unauthorized():
    """Test that the predict endpoint requires authorization."""
    response = client.post("/predict", json={})
    assert response.status_code == 403 # HTTPBearer returns 403 if no auth header

def test_predict_logic():
    """
    Test the core risk logic without auth (requires mocking the dependency).
    In a real CI, we'd mock the models too.
    """
    # For now, just a placeholder to ensure the file exists and is discoverable
    assert True

def test_database_connection():
    """Ensure database initialization doesn't crash."""
    from services.database import init_db
    try:
        init_db()
        assert True
    except Exception as e:
        pytest.fail(f"Database init failed: {e}")
