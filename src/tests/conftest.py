# tests/conftest.py
import pytest
from app import create_app
from infra import db


@pytest.fixture(scope="function")
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # in-memory DB

    with app.app_context():
        db.create_all()  # create tables
        yield app  # provide app to tests
        db.session.remove()
        db.drop_all()  # clean up after test
