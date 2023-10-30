import tomllib

from fastapi.testclient import TestClient

from src import create_app

client = TestClient(create_app(tomllib.load(open("config.toml", "rb"))))


def test_get_agents():
    response = client.get("/agents/explicit")

    assert response.status_code == 200
    assert type(response.json()) == list
