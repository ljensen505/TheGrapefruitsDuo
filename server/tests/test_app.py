from fastapi.testclient import TestClient

from app import app

client = TestClient(app=app)


def test_app():
    assert isinstance(client, TestClient)
