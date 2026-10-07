from fastapi.testclient import TestClient
from app.main import app


def test_root_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome to IntelliShop"
    assert data["documentation"] == "/docs"
    assert data["health"] == "/api/v1/health"