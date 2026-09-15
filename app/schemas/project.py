from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProjectType(str, Enum):
    OFFSHORE = "offshore"
    SES = "ses"
    LAB = "lab"
    NEW_DEV = "new_dev"
    MAINTENANCE = "maintenance"


class DevProcessPhase(str, Enum):
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    RELEASE = "release"
    MAINTENANCE_OPS = "maintenance_ops"


class ProjectCreateInput(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    project_name: str = Field(min_length=1, max_length=255)

    description: str | None = None
    start_date: date
    end_date: date | None = None
    is_ongoing: bool = False

    team_size: int | None = Field(default=None, ge=1)
    total_man_month: float | None = Field(default=None, ge=0)

    source_note: str | None = None
    industry: str | None = Field(default=None, max_length=255)
    outcome_note: str | None = None
    team_composition_note: str | None = None

    technologies: list[str] = Field(default_factory=list)
    project_types: list[ProjectType] = Field(default_factory=list)
    dev_process_phases: list[DevProcessPhase] = Field(default_factory=list)

    @field_validator("customer_name", "project_name")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("must not be blank")

        return cleaned_value

    @model_validator(mode="after")
    def validate_project_dates(self) -> "ProjectCreateInput":
        if self.is_ongoing and self.end_date is not None:
            raise ValueError(
                "end_date must not be provided when is_ongoing is true"
            )

        if (
            self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError(
                "end_date must be on or after start_date"
            )

        return self


class ProjectResponse(BaseModel):
    id: int
    customer_name: str
    project_name: str
    description: str | None = None
    start_date: date
    end_date: date | None = None
    is_ongoing: bool

    team_size: int | None = None
    total_man_month: float | None = None

    source_note: str | None = None
    industry: str | None = None
    outcome_note: str | None = None
    team_composition_note: str | None = None

    technologies: list[str] = Field(default_factory=list)
    project_types: list[ProjectType] = Field(default_factory=list)
    dev_process_phases: list[DevProcessPhase] = Field(default_factory=list)

    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse] = Field(default_factory=list)
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)