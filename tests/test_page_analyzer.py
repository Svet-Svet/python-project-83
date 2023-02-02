import pytest
from page_analyzer.app import app


@pytest.fixture()
def test():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    yield test_app


@pytest.fixture()
def client(test):
    return test.test_client()


def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_request_urls(client):
    response = client.get("/")
    assert response.status_code == 200
