from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TechTag(Base):
    __tablename__ = "tech_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 大文字小文字を区別する（"React" と "react" は別タグ）
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
