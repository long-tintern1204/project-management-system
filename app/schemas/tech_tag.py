from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TechTagResponse(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)