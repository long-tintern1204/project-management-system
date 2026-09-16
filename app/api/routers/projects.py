from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas import ProjectListResponse, ProjectResponse
from app.services import project_query_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=ProjectListResponse, summary="プロジェクト一覧取得")
def list_projects(
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(20, ge=1, le=1000, description="1ページあたりの件数"),
    db: Session = Depends(get_db),
):
    return project_query_service.get_projects(db, page=page, page_size=page_size)


@router.get("/{project_id}", response_model=ProjectResponse, summary="プロジェクト詳細取得")
def get_project(project_id: int, db: Session = Depends(get_db)):
    return project_query_service.get_project_by_id(db, project_id)
