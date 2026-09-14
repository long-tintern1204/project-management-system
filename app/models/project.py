from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[str] = mapped_column(String(10), nullable=False)
    end_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    team_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_man_month: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    outcome_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    team_composition_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 配列は CSV 文字列で保存: ["A","B"] -> "A,B" / [] -> ""
    technologies_csv: Mapped[str] = mapped_column(String(2000), nullable=False, default="", server_default="")
    project_types_csv: Mapped[str] = mapped_column(String(500), nullable=False, default="", server_default="")
    dev_process_phases_csv: Mapped[str] = mapped_column(String(500), nullable=False, default="", server_default="")

    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    # 論理削除: NULL なら有効、値があれば削除済み
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
