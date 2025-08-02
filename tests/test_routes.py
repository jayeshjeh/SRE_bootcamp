
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_healthcheck(client):
    res = client.get("/healthcheck")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


def test_add_student(client):
    response = client.post("/api/v1/students/", json={
        "name": "John",
        "age": 25,
        "grade": "B"
    })
    assert response.status_code == 201
    assert response.json["name"] == "John"
