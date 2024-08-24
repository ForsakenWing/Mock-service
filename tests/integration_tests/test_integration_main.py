import os

import pytest

import requests as client

import json

host = os.getenv("HOST", "127.0.0.1:5555")
base_url = os.getenv("SERVER_URI", f"http://{host}")
headers = {"Accept": "application/json", "Host": host}


def test_get_echo_reply():
    response = client.get(base_url + "/", headers=headers)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>Some HTML in here</title>" in response.text
    assert "<h1>Look ma! HTML!</h1>" in response.text


@pytest.mark.parametrize(
    "test_input", [({"name": "Vasiliy"}), ({"surname": "Petrov"}), ({})]
)
def test_post_echo_reply(test_input):
    response = client.post(base_url + "/", headers=headers, json=test_input)
    assert response.status_code == 200
    assert json.loads(response.json()) == test_input


def test_get_request_parser():
    session = client.Session()
    response = session.get(base_url + "/request", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "headers": {k.lower(): v for k, v in dict(response.request.headers).items()},
        "cookies": dict(session.cookies),
        "method": response.request.method,
        "body": {},
    }


@pytest.mark.parametrize(
    "test_input",
    [
        ({"name": "Vasya", "surname": "Vasiliev"}),
        ({"color": "black", "something": 5}),
        ({}),
    ],
)
def test_post_request_parser(test_input):
    session = client.Session()
    response = client.post(base_url + "/request", headers=headers, json=test_input)
    assert response.status_code == 200
    assert response.json() == {
        "headers": {k.lower(): v for k, v in dict(response.request.headers).items()},
        "cookies": dict(session.cookies),
        "method": response.request.method,
        "body": test_input,
    }
