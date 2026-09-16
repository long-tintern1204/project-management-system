from tests.conftest import make_project

EXPECTED_FIELDS = {
    "id", "customer_name", "project_name", "description", "start_date", "end_date",
    "is_ongoing", "team_size", "total_man_month", "source_note", "industry",
    "outcome_note", "team_composition_note", "technologies", "project_types",
    "dev_process_phases", "created_by", "created_at", "updated_at",
}


# --- 認証 ---

def test_list_requires_token(client):
    assert client.get("/projects").status_code == 401


def test_detail_requires_token(client):
    assert client.get("/projects/1").status_code == 401


# --- GET /projects ---

def test_list_empty(client, auth_headers):
    res = client.get("/projects", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == {"items": [], "total": 0, "page": 1, "page_size": 20}


def test_list_pagination(client, db, auth_headers):
    for i in range(5):
        make_project(db, project_name=f"案件{i}")

    res = client.get("/projects?page=2&page_size=2", headers=auth_headers)
    body = res.json()
    assert res.status_code == 200
    assert body["total"] == 5
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert len(body["items"]) == 2


def test_list_hides_soft_deleted(client, db, auth_headers, soft_deleted_project):
    make_project(db, project_name="有効")

    body = client.get("/projects", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "有効"


def test_list_rejects_invalid_page(client, auth_headers):
    assert client.get("/projects?page=0", headers=auth_headers).status_code == 422
    assert client.get("/projects?page_size=1001", headers=auth_headers).status_code == 422


# --- GET /projects/{id} ---

def test_detail_returns_all_fields(client, db, auth_headers):
    project = make_project(db, team_size=3, total_man_month=4.5)

    res = client.get(f"/projects/{project.id}", headers=auth_headers)
    body = res.json()
    assert res.status_code == 200
    assert set(body) == EXPECTED_FIELDS
    assert body["technologies"] == ["React", "FastAPI"]
    assert body["project_types"] == ["offshore", "new_dev"]
    assert body["dev_process_phases"] == ["design", "implementation"]
    assert body["start_date"] == "2026-01-01"
    assert body["end_date"] is None
    assert body["total_man_month"] == 4.5


def test_detail_empty_csv_becomes_empty_list(client, db, auth_headers):
    project = make_project(db, technologies_csv="", project_types_csv="", dev_process_phases_csv="")

    body = client.get(f"/projects/{project.id}", headers=auth_headers).json()
    assert body["technologies"] == []
    assert body["project_types"] == []
    assert body["dev_process_phases"] == []


def test_detail_not_found(client, auth_headers):
    res = client.get("/projects/9999", headers=auth_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "プロジェクトが見つかりません"


def test_detail_soft_deleted_is_404(client, auth_headers, soft_deleted_project):
    assert client.get(f"/projects/{soft_deleted_project.id}", headers=auth_headers).status_code == 404


def test_detail_blank_end_date_becomes_null(client, db, auth_headers):
    project = make_project(db, end_date="")

    body = client.get(f"/projects/{project.id}", headers=auth_headers).json()
    assert body["end_date"] is None


def test_list_accepts_page_size_1000(client, auth_headers):
    res = client.get("/projects?page_size=1000", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["page_size"] == 1000
