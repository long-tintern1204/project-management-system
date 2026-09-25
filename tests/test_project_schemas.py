import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreateInput


# Dữ liệu Project hợp lệ dùng chung
def create_valid_project_data():
    return {
        "customer_name": "VNEXT",
        "project_name": "Project Management System",
        "description": "Internal training project",
        "start_date": "2026-09-01",
        "end_date": "2026-12-31",
        "is_ongoing": False,
        "team_size": 3,
        "total_man_month": 6.5,
        "source_note": "Training",
        "industry": "IT",
        "outcome_note": "Complete project",
        "team_composition_note": "Three members",
        "technologies": ["Python", "FastAPI"],
        "project_types": ["new_dev"],
        "dev_process_phases": ["implementation", "testing"],
    }


# 1. Kiểm tra dữ liệu Project hợp lệ
def test_project_create_valid_data():
    payload = create_valid_project_data()

    project = ProjectCreateInput(**payload)

    assert project.customer_name == "VNEXT"
    assert project.project_name == "Project Management System"
    assert project.total_man_month == 6.5
    assert project.technologies == ["Python", "FastAPI"]


# 2. Kiểm tra cho phép các mảng rỗng
def test_project_create_allows_empty_lists():
    payload = create_valid_project_data()
    payload["technologies"] = []
    payload["project_types"] = []
    payload["dev_process_phases"] = []

    project = ProjectCreateInput(**payload)

    assert project.technologies == []
    assert project.project_types == []
    assert project.dev_process_phases == []


# 3. Kiểm tra customer_name không được để trống
def test_customer_name_must_not_be_blank():
    payload = create_valid_project_data()
    payload["customer_name"] = "   "

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "空白のみの値は入力できません" in str(error.value)


# 4. Kiểm tra project_name không được để trống
def test_project_name_must_not_be_blank():
    payload = create_valid_project_data()
    payload["project_name"] = "   "

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "空白のみの値は入力できません" in str(error.value)


# 5. Kiểm tra end_date không được trước start_date
def test_end_date_must_be_after_start_date():
    payload = create_valid_project_data()
    payload["start_date"] = "2026-09-10"
    payload["end_date"] = "2026-09-09"

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "終了日は開始日以降の日付を指定してください" in str(
        error.value
    )


# 6. Kiểm tra dự án đang thực hiện không được nhập end_date
def test_ongoing_project_must_not_have_end_date():
    payload = create_valid_project_data()
    payload["is_ongoing"] = True
    payload["end_date"] = "2026-12-31"

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "進行中のプロジェクトには終了日を設定できません" in str(
        error.value
    )


# 7. Kiểm tra dự án đang thực hiện hợp lệ khi end_date là null
def test_ongoing_project_accepts_null_end_date():
    payload = create_valid_project_data()
    payload["is_ongoing"] = True
    payload["end_date"] = None

    project = ProjectCreateInput(**payload)

    assert project.is_ongoing is True
    assert project.end_date is None


# 8. Kiểm tra total_man_month không được là số âm
def test_total_man_month_must_not_be_negative():
    payload = create_valid_project_data()
    payload["total_man_month"] = -1

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "total_man_month" in str(error.value)


# 9. Kiểm tra project_types sai Enum
def test_project_type_must_be_valid():
    payload = create_valid_project_data()
    payload["project_types"] = ["invalid_type"]

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "project_types" in str(error.value)


# 10. Kiểm tra dev_process_phases sai Enum
def test_dev_process_phase_must_be_valid():
    payload = create_valid_project_data()
    payload["dev_process_phases"] = ["invalid_phase"]

    with pytest.raises(ValidationError) as error:
        ProjectCreateInput(**payload)

    assert "dev_process_phases" in str(error.value)