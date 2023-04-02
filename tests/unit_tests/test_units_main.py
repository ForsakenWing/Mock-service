import json

import pytest

from src.main import app

from fastapi.testclient import TestClient

headers = {"Accept": "application/json"}
client = TestClient(app, headers=headers)


def test_get_echo_reply():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, stranger"}


@pytest.mark.parametrize("test_input", [
    ({"name": "Vasiliy"}),
    ({"surname": "Petrov"}),
    ({})
])
def test_post_echo_reply(test_input):
    response = client.post('/',  json=test_input)
    assert response.status_code == 200
    assert json.loads(response.json()) == test_input


def test_get_request_parser():
    response = client.get('/request')
    assert response.status_code == 200
    assert response.json() == {
        "headers": dict(response.request.headers),
        "cookies": dict(client.cookies),
        "method": response.request.method,
        "body": {}
    }


@pytest.mark.parametrize("test_input", [
    ({"name": "Vasya", "surname": "Vasiliev"}),
    ({"color": "black", "something": 5}),
    ({})
])
def test_post_request_parser(test_input):
    response = client.post('/request', json=test_input)
    assert response.status_code == 200
    assert response.json() == {
        "headers": dict(response.request.headers),
        "cookies": dict(client.cookies),
        "method": response.request.method,
        "body": test_input
    }
