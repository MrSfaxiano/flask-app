import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0


def test_get_task_found(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json["id"] == 1


def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "error" in response.json


def test_get_done_tasks(client):
    response = client.get("/tasks/done")
    assert response.status_code == 200
    assert all(t["done"] for t in response.json)
