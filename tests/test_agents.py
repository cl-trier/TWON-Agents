import tomllib

import pytest
from fastapi.testclient import TestClient

from src import create_app

client = TestClient(create_app(tomllib.load(open("config.toml", "rb"))))


def test_get_agents():
    response = client.get("/agents/explicit")
    data = response.json()

    assert response.status_code == 200
    assert type(data) == list
    assert all([set(data[n].keys()) == set(data[n + 1].keys()) for n in range(len(data) - 1)])
    assert set(response.json()[0].keys()) == {'id', 'name', 'character'}


@pytest.mark.skip(reason="Need to define test results")
def test_get_agent():
    response = client.get("/agents/explicit/?name=base&action=reply&content=Hallo")

    assert response.status_code == 200
    assert type(response.json()) == dict
