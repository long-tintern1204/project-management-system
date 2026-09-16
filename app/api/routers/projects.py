from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.project import Project
from app.schemas.project import (
    ProjectCreateInput,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdateInput,
)
from app.services import project_query_service
from app.services.project_service import upsert_tech_tags


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)],
)


def list_to_csv(values: list[str]) -> str:
    return ",".join(values)


def csv_to_list(value: str | None) -> list[str]:
    if not value:
        return []

    return value.split(",")


def project_to_response(project: Project) -> ProjectResponse:
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
        dev_process_phases=csv_to_list(
            project.dev_process_phases_csv
        ),
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def update_project_fields(
    project: Project,
    project_input: ProjectCreateInput | ProjectUpdateInput,
    technologies: list[str],
) -> None:
    project.customer_name = project_input.customer_name
    project.project_name = project_input.project_name
    project.description = project_input.description

    # Model hiện tại lưu ngày dưới dạng chuỗi ISO (YYYY-MM-DD).
    project.start_date = project_input.start_date.isoformat()
    project.end_date = (
        project_input.end_date.isoformat()
        if project_input.end_date is not None
        else None
    )

    project.is_ongoing = project_input.is_ongoing
    project.team_size = project_input.team_size
    project.total_man_month = project_input.total_man_month
    project.source_note = project_input.source_note
    project.industry = project_input.industry
    project.outcome_note = project_input.outcome_note
    project.team_composition_note = (
        project_input.team_composition_note
    )

    project.technologies_csv = list_to_csv(technologies)
    project.project_types_csv = list_to_csv(
        [item.value for item in project_input.project_types]
    )
    project.dev_process_phases_csv = list_to_csv(
        [item.value for item in project_input.dev_process_phases]
    )


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="プロジェクト一覧取得",
)
def list_projects(
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(
        20,
        ge=1,
        le=1000,
        description="1ページあたりの件数",
    ),
    db: Session = Depends(get_db),
):
    return project_query_service.get_projects(
        db,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="プロジェクト詳細取得",
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return project_query_service.get_project_by_id(db, project_id)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_input: ProjectCreateInput,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ProjectResponse:
    technologies = upsert_tech_tags(
        db,
        project_input.technologies,
    )

    project = Project(
        customer_name=project_input.customer_name,
        project_name=project_input.project_name,
        start_date=project_input.start_date.isoformat(),
        created_by=current_user["email"],
    )

    update_project_fields(
        project,
        project_input,
        technologies,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project_to_response(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    project_input: ProjectUpdateInput,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.deleted_at.is_(None),
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="プロジェクトが見つかりません",
        )

    technologies = upsert_tech_tags(
        db,
        project_input.technologies,
    )

    update_project_fields(
        project,
        project_input,
        technologies,
    )

    db.commit()
    db.refresh(project)

    return project_to_response(project)
