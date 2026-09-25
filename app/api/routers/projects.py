from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.project import (
    ProjectCreateInput,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdateInput,
)
from app.services import project_query_service, project_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)],
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
    q: str | None = Query(
        None,
        description="全文検索（customer_name / project_name / description の部分一致）",
    ),
    technology: list[str] | None = Query(
        None,
        description="技術で絞り込み（同一項目内は OR）",
    ),
    project_type: list[str] | None = Query(
        None,
        description="種別で絞り込み（同一項目内は OR）",
    ),
    dev_process_phase: list[str] | None = Query(
        None,
        description="開発工程で絞り込み（同一項目内は OR）",
    ),
    db: Session = Depends(get_db),
):
    return project_query_service.get_projects(
        db,
        page=page,
        page_size=page_size,
        q=q,
        technologies=technology,
        project_types=project_type,
        dev_process_phases=dev_process_phase,
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
    return project_service.create_project(
        db=db,
        project_input=project_input,
        created_by=current_user["email"],
    )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    project_input: ProjectUpdateInput,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = project_service.update_project(
        db=db,
        project_id=project_id,
        project_input=project_input,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="プロジェクトが見つかりません",
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="プロジェクト削除")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project_service.delete_project(db, project_id)
    return None