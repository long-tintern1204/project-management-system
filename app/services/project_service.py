from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project


def delete_project(db: Session, project_id: int) -> None:
    """Thực hiện xóa mềm (Soft Delete) dự án theo ID"""
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.deleted_at.is_(None))
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="プロジェクトが見つかりません",
        )
    project.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    