from datetime import datetime

from pydantic import BaseModel


class TechTagResponse(BaseModel):
    id: int
    name: str
    created_at: datetime


class TechTagListResponse(BaseModel):
    items: list[str]