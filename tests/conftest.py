import os
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Project  # noqa: E402

# テスト専用のインメモリ DB（StaticPool で全接続が同じ DB を共有）
_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSession = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=_engine)
    session = _TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=_engine)


@pytest.fixture()
def client(db):
    def _override_get_db():
        yield db

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    res = client.post(
        "/auth/register",
        json={"email": "tester@example.com", "password": "Password123"},
    )
    if res.status_code == 409:
        res = client.post(
            "/auth/login",
            json={"email": "tester@example.com", "password": "Password123"},
        )
    return {"Authorization": f"Bearer {res.json()['idToken']}"}


def make_project(db, **overrides) -> Project:
    data = dict(
        customer_name="顧客A",
        project_name="案件A",
        start_date="2026-01-01",
        is_ongoing=False,
        technologies_csv="React,FastAPI",
        project_types_csv="offshore,new_dev",
        dev_process_phases_csv="design,implementation",
        created_by="tester@example.com",
    )
    data.update(overrides)
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@pytest.fixture()
def soft_deleted_project(db) -> Project:
    return make_project(db, project_name="削除済み", deleted_at=datetime(2026, 2, 1))
