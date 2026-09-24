from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services import tech_tag_service


router = APIRouter(
    prefix="/tech-tags",
    tags=["Tech Tags"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=list[str],
    summary="技術タグ候補取得",
)
def autocomplete_tech_tags(
    q: str = Query(
        default="",
        description="検索キーワード（大文字・小文字を区別しません）",
    ),
    db: Session = Depends(get_db),
) -> list[str]:
    return tech_tag_service.autocomplete_tech_tags(
        db=db,
        q=q,
    )