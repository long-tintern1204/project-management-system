from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tech_tag import TechTag


def autocomplete_tech_tags(
    db: Session,
    q: str = "",
) -> list[str]:
    keyword = q.strip()

    statement = select(TechTag.name)

    if keyword:
        statement = statement.where(
            TechTag.name.ilike(f"%{keyword}%")
        )

    statement = statement.order_by(
        TechTag.created_at.desc(),
        TechTag.id.desc(),
    ).limit(20)

    return list(db.scalars(statement).all())