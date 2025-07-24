import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure JWT signing key is present
os.environ.setdefault("MOOLAH_SECRET_KEY", "test-secret")
# Use a temporary SQLite database
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
# Allow importing backend code
sys.path.append(str(Path(__file__).resolve().parent.parent / "moolah_backend"))

from app.main import app
from app.database import Base, engine, SessionLocal
from app import models


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine.dispose()


@pytest.fixture
def auth_headers(client):
    def _create_headers(email="user@example.com", password="secret", is_admin=False):
        client.post(
            "/users/",
            json={"email": email, "password": password, "is_admin": is_admin},
        )
        if is_admin:
            db = SessionLocal()
            user = db.query(models.User).filter(models.User.email == email).first()
            if user:
                user.is_admin = True
                db.commit()
            db.close()
        res = client.post(
            "/token",
            data={"username": email, "password": password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        token = res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _create_headers
