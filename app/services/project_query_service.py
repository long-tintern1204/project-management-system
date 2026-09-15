from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Project
from app.schemas import ProjectListResponse, ProjectResponse


def csv_to_list(value: str | None) -> list[str]:
    """"A,B" -> ["A","B"] / "" や None -> []"""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        customer_name=project.customer_name,
        project_name=project.project_name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
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


def get_projects(db: Session, page: int = 1, page_size: int = 20) -> ProjectListResponse:
    active = Project.deleted_at.is_(None)

    total = db.scalar(select(func.count()).select_from(Project).where(active)) or 0
    rows = db.scalars(
        select(Project)
        .where(active)
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
