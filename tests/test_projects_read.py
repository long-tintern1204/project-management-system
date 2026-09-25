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


# --- W11: 全文検索 q ---

def test_search_matches_customer_name(client, db, auth_headers):
    make_project(db, customer_name="株式会社アルファ", project_name="案件1")
    make_project(db, customer_name="株式会社ベータ", project_name="案件2")

    body = client.get("/projects?q=アルファ", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["customer_name"] == "株式会社アルファ"


def test_search_matches_project_name(client, db, auth_headers):
    make_project(db, project_name="Web刷新プロジェクト")
    make_project(db, project_name="基幹システム保守")

    body = client.get("/projects?q=刷新", headers=auth_headers).json()
    assert body["total"] == 1


def test_search_matches_description(client, db, auth_headers):
    make_project(db, project_name="案件1", description="ECサイトの構築案件")
    make_project(db, project_name="案件2", description=None)

    body = client.get("/projects?q=ECサイト", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "案件1"


def test_search_is_case_insensitive(client, db, auth_headers):
    make_project(db, project_name="Renewal Project")

    for keyword in ("renewal", "RENEWAL", "ReNeWaL"):
        body = client.get(f"/projects?q={keyword}", headers=auth_headers).json()
        assert body["total"] == 1, keyword


def test_search_no_match_returns_empty(client, db, auth_headers):
    make_project(db, project_name="案件A")

    body = client.get("/projects?q=存在しない", headers=auth_headers).json()
    assert body == {"items": [], "total": 0, "page": 1, "page_size": 20}


def test_search_treats_percent_as_literal(client, db, auth_headers):
    make_project(db, project_name="進捗100%完了")
    make_project(db, project_name="通常案件")

    body = client.get("/projects?q=%25", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "進捗100%完了"


def test_search_blank_is_ignored(client, db, auth_headers):
    make_project(db, project_name="案件A")
    make_project(db, project_name="案件B")

    assert client.get("/projects?q=", headers=auth_headers).json()["total"] == 2
    assert client.get("/projects?q=%20%20", headers=auth_headers).json()["total"] == 2


def test_search_excludes_soft_deleted(client, db, auth_headers):
    from datetime import datetime

    make_project(db, project_name="削除対象案件", deleted_at=datetime(2026, 2, 1))
    make_project(db, project_name="有効案件")

    body = client.get("/projects?q=案件", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "有効案件"


# --- W11: 絞り込み（同一項目内 OR） ---

def test_filter_single_technology(client, db, auth_headers):
    make_project(db, project_name="React案件", technologies_csv="React,TypeScript")
    make_project(db, project_name="Java案件", technologies_csv="Java,Spring")

    body = client.get("/projects?technology=React", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "React案件"


def test_filter_technologies_is_or(client, db, auth_headers):
    make_project(db, project_name="React案件", technologies_csv="React")
    make_project(db, project_name="Vue案件", technologies_csv="Vue")
    make_project(db, project_name="Java案件", technologies_csv="Java")

    body = client.get("/projects?technology=React&technology=Vue", headers=auth_headers).json()
    assert body["total"] == 2
    assert {item["project_name"] for item in body["items"]} == {"React案件", "Vue案件"}


def test_filter_does_not_match_partial_token(client, db, auth_headers):
    """Java で絞り込んでも JavaScript はヒットしない"""
    make_project(db, project_name="JS案件", technologies_csv="JavaScript,React")
    make_project(db, project_name="Java案件", technologies_csv="Java,Spring")

    body = client.get("/projects?technology=Java", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "Java案件"


def test_filter_is_case_insensitive(client, db, auth_headers):
    make_project(db, project_name="React案件", technologies_csv="React")

    assert client.get("/projects?technology=react", headers=auth_headers).json()["total"] == 1
    assert client.get("/projects?technology=REACT", headers=auth_headers).json()["total"] == 1


def test_filter_project_types(client, db, auth_headers):
    make_project(db, project_name="オフショア案件", project_types_csv="offshore")
    make_project(db, project_name="SES案件", project_types_csv="ses")

    body = client.get("/projects?project_type=offshore", headers=auth_headers).json()
    assert body["total"] == 1


def test_filter_dev_process_phases(client, db, auth_headers):
    make_project(db, project_name="設計案件", dev_process_phases_csv="design")
    make_project(db, project_name="テスト案件", dev_process_phases_csv="testing")

    body = client.get("/projects?dev_process_phase=testing", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "テスト案件"


# --- W11: 絞り込み（項目間 AND） ---

def test_filter_across_fields_is_and(client, db, auth_headers):
    make_project(db, project_name="両方一致", technologies_csv="React", project_types_csv="offshore")
    make_project(db, project_name="技術のみ一致", technologies_csv="React", project_types_csv="ses")
    make_project(db, project_name="種別のみ一致", technologies_csv="Vue", project_types_csv="offshore")

    body = client.get(
        "/projects?technology=React&project_type=offshore", headers=auth_headers
    ).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "両方一致"


def test_filter_three_fields_combined(client, db, auth_headers):
    make_project(
        db,
        project_name="全条件一致",
        technologies_csv="React,Node.js",
        project_types_csv="offshore",
        dev_process_phases_csv="design,testing",
    )
    make_project(
        db,
        project_name="工程が不一致",
        technologies_csv="React",
        project_types_csv="offshore",
        dev_process_phases_csv="release",
    )

    body = client.get(
        "/projects?technology=React&project_type=offshore&dev_process_phase=testing",
        headers=auth_headers,
    ).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "全条件一致"


def test_search_and_filter_combined(client, db, auth_headers):
    make_project(db, project_name="EC刷新", technologies_csv="React")
    make_project(db, project_name="EC保守", technologies_csv="Java")
    make_project(db, project_name="社内ツール", technologies_csv="React")

    body = client.get("/projects?q=EC&technology=React", headers=auth_headers).json()
    assert body["total"] == 1
    assert body["items"][0]["project_name"] == "EC刷新"


def test_filter_empty_value_is_ignored(client, db, auth_headers):
    make_project(db, project_name="案件A")
    make_project(db, project_name="案件B")

    assert client.get("/projects?technology=", headers=auth_headers).json()["total"] == 2


def test_filter_unknown_value_returns_empty(client, db, auth_headers):
    make_project(db, technologies_csv="React")

    body = client.get("/projects?technology=COBOL", headers=auth_headers).json()
    assert body == {"items": [], "total": 0, "page": 1, "page_size": 20}


def test_filter_respects_pagination(client, db, auth_headers):
    for i in range(5):
        make_project(db, project_name=f"React案件{i}", technologies_csv="React")
    make_project(db, project_name="Java案件", technologies_csv="Java")

    body = client.get(
        "/projects?technology=React&page=2&page_size=2", headers=auth_headers
    ).json()
    assert body["total"] == 5
    assert body["page"] == 2
    assert len(body["items"]) == 2


# --- W11: ページング境界 ---

def test_page_size_1000_is_accepted(client, auth_headers):
    res = client.get("/projects?page_size=1000", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["page_size"] == 1000


def test_page_size_over_1000_is_422(client, auth_headers):
    assert client.get("/projects?page_size=1001", headers=auth_headers).status_code == 422


def test_page_and_page_size_lower_bounds(client, auth_headers):
    assert client.get("/projects?page=0", headers=auth_headers).status_code == 422
    assert client.get("/projects?page_size=0", headers=auth_headers).status_code == 422
