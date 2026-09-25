"""Tests for POST /projects and PUT /projects/{project_id}."""

from datetime import datetime, timezone

from sqlalchemy import select

from app.models.project import Project
from app.models.tech_tag import TechTag


def valid_project_payload(**overrides):
    """Return valid request data that individual tests can customize."""
    payload = {
        "customer_name": "VNEXT",
        "project_name": "Project Management System",
        "description": "W10 API test",
        "start_date": "2026-09-01",
        "end_date": "2026-12-31",
        "is_ongoing": False,
        "team_size": 3,
        "total_man_month": 6.5,
        "source_note": "pytest",
        "industry": "IT",
        "outcome_note": "Backend implementation",
        "team_composition_note": "Three members",
        "technologies": [" Python ", "FastAPI", "React", "react", "Python"],
        "project_types": ["new_dev"],
        "dev_process_phases": ["implementation", "testing"],
    }
    payload.update(overrides)
    return payload


def test_create_requires_token(client):
    response = client.post("/projects", json=valid_project_payload())

    assert response.status_code == 401


def test_create_project_success_and_upsert_tags(
    client,
    db,
    auth_headers,
):
    response = client.post(
        "/projects",
        json=valid_project_payload(),
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.json()

    assert body["id"] > 0
    assert body["customer_name"] == "VNEXT"
    assert body["project_name"] == "Project Management System"
    assert body["created_by"] == "tester@example.com"
    assert body["technologies"] == ["Python", "FastAPI", "React", "react"]
    assert body["project_types"] == ["new_dev"]
    assert body["dev_process_phases"] == ["implementation", "testing"]

    # Khoảng trắng và tag trùng hoàn toàn đã bị loại bỏ.
    # React và react vẫn là hai tag khác nhau (case-sensitive).
    tag_names = db.scalars(
        select(TechTag.name).order_by(TechTag.name)
    ).all()
    assert tag_names == ["FastAPI", "Python", "React", "react"]

    project = db.get(Project, body["id"])
    assert project is not None
    assert project.technologies_csv == "Python,FastAPI,React,react"
    assert project.project_types_csv == "new_dev"
    assert project.dev_process_phases_csv == "implementation,testing"
    assert project.created_by == "tester@example.com"


def test_create_reuses_existing_tech_tag(client, db, auth_headers):
    db.add(TechTag(name="FastAPI"))
    db.commit()

    response = client.post(
        "/projects",
        json=valid_project_payload(technologies=["FastAPI", "SQLAlchemy"]),
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["technologies"] == ["FastAPI", "SQLAlchemy"]
    assert len(db.scalars(select(TechTag)).all()) == 2


def test_create_rejects_invalid_dates(client, auth_headers):
    payload = valid_project_payload(
        start_date="2026-09-10",
        end_date="2026-09-09",
    )

    response = client.post(
        "/projects",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_rejects_end_date_for_ongoing_project(client, auth_headers):
    payload = valid_project_payload(is_ongoing=True)

    response = client.post(
        "/projects",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_rejects_negative_total_man_month(client, auth_headers):
    response = client.post(
        "/projects",
        json=valid_project_payload(total_man_month=-0.5),
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_project_success_and_sync_tags(client, db, auth_headers):
    create_response = client.post(
        "/projects",
        json=valid_project_payload(technologies=["Python", "FastAPI"]),
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    update_payload = valid_project_payload(
        project_name="Updated Project",
        end_date=None,
        is_ongoing=True,
        total_man_month=8.0,
        technologies=[" FastAPI ", "SQLAlchemy", "sqlalchemy"],
        project_types=["maintenance"],
        dev_process_phases=["maintenance_ops"],
    )

    response = client.put(
        f"/projects/{project_id}",
        json=update_payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == project_id
    assert body["project_name"] == "Updated Project"
    assert body["is_ongoing"] is True
    assert body["end_date"] is None
    assert body["total_man_month"] == 8.0
    assert body["technologies"] == ["FastAPI", "SQLAlchemy", "sqlalchemy"]
    assert body["project_types"] == ["maintenance"]
    assert body["dev_process_phases"] == ["maintenance_ops"]
    assert body["created_by"] == "tester@example.com"

    db.expire_all()
    project = db.get(Project, project_id)
    assert project is not None
    assert project.technologies_csv == "FastAPI,SQLAlchemy,sqlalchemy"

    tag_names = set(db.scalars(select(TechTag.name)).all())
    assert tag_names == {"Python", "FastAPI", "SQLAlchemy", "sqlalchemy"}


def test_update_requires_token(client):
    response = client.put(
        "/projects/1",
        json=valid_project_payload(),
    )

    assert response.status_code == 401


def test_update_returns_404_when_project_does_not_exist(client, auth_headers):
    response = client.put(
        "/projects/999999",
        json=valid_project_payload(),
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "プロジェクトが見つかりません"


def test_update_returns_404_for_soft_deleted_project(
    client,
    db,
    auth_headers,
):
    create_response = client.post(
        "/projects",
        json=valid_project_payload(),
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    project = db.get(Project, project_id)
    project.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()

    response = client.put(
        f"/projects/{project_id}",
        json=valid_project_payload(project_name="Must not update"),
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "プロジェクトが見つかりません"
