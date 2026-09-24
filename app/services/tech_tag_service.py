from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.tech_tag import TechTag
from app.utils.sql import LIKE_ESCAPE, escape_like


def autocomplete_tech_tags(
    db: Session,
    q: str = "",
) -> list[str]:
    keyword = q.strip()

    statement = select(TechTag.name)

    if keyword:
        escaped_keyword = escape_like(keyword)

        statement = statement.where(
            TechTag.name.ilike(
                f"%{escaped_keyword}%",
                escape=LIKE_ESCAPE,
            )
        )

    statement = statement.order_by(
        func.lower(TechTag.name).asc(),
        TechTag.name.asc(),
    ).limit(20)

    return list(db.scalars(statement).all())
