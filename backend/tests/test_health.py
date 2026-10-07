from fastapi.testclient import TestClient
from app.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "IntelliShop"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"