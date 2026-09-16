from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tech_tag import TechTag


def upsert_tech_tags(
    db: Session,
    technologies: list[str],
) -> list[str]:
    """
    Chuẩn hóa và thêm các technology tag chưa tồn tại.

    Phân biệt chữ hoa và chữ thường:
    "React" và "react" được xem là hai tag khác nhau.
    """
    cleaned_tags: list[str] = []
    seen_tags: set[str] = set()

    for technology in technologies:
        cleaned_name = technology.strip()

        # Bỏ qua tag rỗng sau khi loại bỏ khoảng trắng
        if not cleaned_name:
            continue

        # Loại bỏ tag trùng hoàn toàn trong cùng request
        if cleaned_name in seen_tags:
            continue

        seen_tags.add(cleaned_name)
        cleaned_tags.append(cleaned_name)

        existing_tag = db.scalar(
            select(TechTag).where(
                TechTag.name == cleaned_name
            )
        )

        if existing_tag is None:
            db.add(TechTag(name=cleaned_name))

    return cleaned_tags