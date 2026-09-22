from fastapi import HTTPException, status
from sqlalchemy import ColumnElement, and_, func, literal, or_, select
from sqlalchemy.orm import Session

from app.models import Project
from app.schemas import ProjectListResponse, ProjectResponse

_LIKE_ESCAPE = "\\"


def csv_to_list(value: str | None) -> list[str]:
    """Giải nén chuỗi CSV: "A,B" -> ["A","B"] / "" hoặc None -> []"""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _escape_like(value: str) -> str:
    """Escape ký tự đại diện của LIKE (% _) để coi chúng là ký tự tìm kiếm bình thường"""
    return (
        value.replace(_LIKE_ESCAPE, _LIKE_ESCAPE * 2)
        .replace("%", _LIKE_ESCAPE + "%")
        .replace("_", _LIKE_ESCAPE + "_")
    )


def _keyword_condition(keyword: str) -> ColumnElement[bool]:
    """Tìm một phần trên customer_name / project_name / description, không phân biệt hoa thường"""
    pattern = f"%{_escape_like(keyword.strip().lower())}%"
    return or_(
        func.lower(Project.customer_name).like(pattern, escape=_LIKE_ESCAPE),
        func.lower(Project.project_name).like(pattern, escape=_LIKE_ESCAPE),
        func.lower(func.coalesce(Project.description, "")).like(pattern, escape=_LIKE_ESCAPE),
    )


def _csv_contains(column, value: str) -> ColumnElement[bool]:
    """Khớp đúng một phần tử trong cột CSV.

    Bọc dấu phẩy hai đầu nên lọc "Java" không khớp nhầm "JavaScript".
    """
    pattern = f"%,{_escape_like(value.strip().lower())},%"
    return (literal(",") + func.lower(column) + literal(",")).like(pattern, escape=_LIKE_ESCAPE)


def _csv_filter(column, values: list[str] | None) -> ColumnElement[bool] | None:
    """OR giữa các giá trị trong cùng một trường. Bỏ qua chuỗi rỗng; không còn giá trị nào thì không lọc"""
    if not values:
        return None
    conditions = [_csv_contains(column, v) for v in values if v and v.strip()]
    if not conditions:
        return None
    return or_(*conditions)


def build_filters(
    q: str | None = None,
    technologies: list[str] | None = None,
    project_types: list[str] | None = None,
    dev_process_phases: list[str] | None = None,
) -> list[ColumnElement[bool]]:
    """Loại bỏ bản ghi xoá mềm, nối từ khoá và các bộ lọc bằng AND"""
    filters: list[ColumnElement[bool]] = [Project.deleted_at.is_(None)]

    if q and q.strip():
        filters.append(_keyword_condition(q))

    for column, values in (
        (Project.technologies_csv, technologies),
        (Project.project_types_csv, project_types),
        (Project.dev_process_phases_csv, dev_process_phases),
    ):
        condition = _csv_filter(column, values)
        if condition is not None:
            filters.append(condition)

    return filters


def to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        customer_name=project.customer_name,
        project_name=project.project_name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date or None,
        is_ongoing=project.is_ongoing,
        team_size=project.team_size,
        total_man_month=project.total_man_month,
        source_note=project.source_note,
        industry=project.industry,
        outcome_note=project.outcome_note,
        team_composition_note=project.team_composition_note,
        technologies=csv_to_list(project.technologies_csv),
        project_types=csv_to_list(project.project_types_csv),
        dev_process_phases=csv_to_list(project.dev_process_phases_csv),
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def get_projects(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    q: str | None = None,
    technologies: list[str] | None = None,
    project_types: list[str] | None = None,
    dev_process_phases: list[str] | None = None,
) -> ProjectListResponse:
    filters = build_filters(
        q=q,
        technologies=technologies,
        project_types=project_types,
        dev_process_phases=dev_process_phases,
    )
    where = and_(*filters)

    total = db.scalar(select(func.count()).select_from(Project).where(where)) or 0
    rows = db.scalars(
        select(Project)
        .where(where)
        .order_by(Project.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return ProjectListResponse(
        items=[to_response(p) for p in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


def get_project_by_id(db: Session, project_id: int) -> ProjectResponse:
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.deleted_at.is_(None))
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="プロジェクトが見つかりません",
        )
    return to_response(project)
