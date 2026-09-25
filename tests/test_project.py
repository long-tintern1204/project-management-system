from sqlalchemy import select
from app.models import Project, TechTag
from tests.conftest import make_project


def test_delete_requires_token(client, db):
    """1. Gọi DELETE /projects/{id} mà không có Bearer token phải trả về 401 Unauthorized"""
    project = make_project(db, project_name="Token Check")
    res = client.delete(f"/projects/{project.id}")
    assert res.status_code == 401
    assert res.json()["detail"] == "認証されていません"


def test_delete_project_success(client, db, auth_headers):
    """2. Xóa mềm thành công: trả về 204, bản ghi vẫn còn trong DB với deleted_at IS NOT NULL"""
    project = make_project(db, project_name="To be deleted")
    project_id = project.id

    # Thực hiện xóa
    res = client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert res.status_code == 204

    # Kiểm tra trong DB: không bị DELETE vật lý, deleted_at đã có giá trị
    db_project = db.scalar(select(Project).where(Project.id == project_id))
    assert db_project is not None
    assert db_project.deleted_at is not None

    # Gọi GET chi tiết dự án đó phải trả về 404
    res_get = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.json()["detail"] == "プロジェクトが見つかりません"


def test_delete_project_not_found(client, auth_headers):
    """3. Xóa một dự án không tồn tại phải trả về 404 Not Found"""
    res = client.delete("/projects/99999", headers=auth_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "プロジェクトが見つかりません"


def test_delete_already_soft_deleted_project(client, auth_headers, soft_deleted_project):
    """4. Xóa một dự án đã bị xóa mềm trước đó phải trả về 404 Not Found"""
    res = client.delete(f"/projects/{soft_deleted_project.id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "プロジェクトが見つかりません"


def test_delete_project_preserves_tech_tags(client, db, auth_headers):
    """5. Xóa mềm dự án không được làm mất các tag công nghệ trong bảng tech_tags (theo Q&A Q4)"""
    # Thêm tag vào bảng tech_tags
    tag = TechTag(name="Kubernetes")
    db.add(tag)
    db.commit()

    project = make_project(db, project_name="Tag Preserve Test", technologies_csv="Kubernetes")
    
    # Xóa dự án
    res = client.delete(f"/projects/{project.id}", headers=auth_headers)
    assert res.status_code == 204

    # Kiểm tra tag vẫn còn nguyên trong bảng tech_tags
    tag_in_db = db.scalar(select(TechTag).where(TechTag.name == "Kubernetes"))
    assert tag_in_db is not None