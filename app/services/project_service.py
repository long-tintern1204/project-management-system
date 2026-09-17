from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.tech_tag import TechTag
from app.schemas.project import (
    ProjectCreateInput,
    ProjectResponse,
    ProjectUpdateInput,
)


def list_to_csv(values: list[str]) -> str:
    return ",".join(values)


def csv_to_list(value: str | None) -> list[str]:
    if not value:
        return []

    return value.split(",")


def upsert_tech_tags(
    db: Session,
    technologies: list[str],
) -> list[str]:
    cleaned_tags: list[str] = []
    seen_tags: set[str] = set()

    for technology in technologies:
        cleaned_name = technology.strip()

        if not cleaned_name or cleaned_name in seen_tags:
            continue

        seen_tags.add(cleaned_name)
        cleaned_tags.append(cleaned_name)

        existing_tag = db.scalar(
            select(TechTag).where(TechTag.name == cleaned_name)
        )

        if existing_tag is None:
            db.add(TechTag(name=cleaned_name))

    return cleaned_tags


def project_to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        customer_name=project.customer_name,
        project_name=project.project_name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        is_ongoing=project.is_ongoing,
        team_size=project.team_size,
        total_man_month=project.total_man_month,
        source_note=project.source_note,
        industry=project.industry,
        outcome_note=project.outcome_note,
        team_composition_note=project.team_composition_note,
        technologies=csv_to_list(project.technologies_csv),
        project_types=csv_to_list(project.project_types_csv),
        dev_process_phases=csv_to_list(
            project.dev_process_phases_csv
        ),
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def update_project_fields(
    project: Project,
    project_input: ProjectCreateInput | ProjectUpdateInput,
    technologies: list[str],
) -> None:
    project.customer_name = project_input.customer_name
    project.project_name = project_input.project_name
    project.description = project_input.description
    project.start_date = project_input.start_date.isoformat()
    project.end_date = (
        project_input.end_date.isoformat()
        if project_input.end_date is not None
        else None
    )
    project.is_ongoing = project_input.is_ongoing
    project.team_size = project_input.team_size
    project.total_man_month = project_input.total_man_month
    project.source_note = project_input.source_note
    project.industry = project_input.industry
    project.outcome_note = project_input.outcome_note
    project.team_composition_note = project_input.team_composition_note

    project.technologies_csv = list_to_csv(technologies)
    project.project_types_csv = list_to_csv(
        [item.value for item in project_input.project_types]
    )
    project.dev_process_phases_csv = list_to_csv(
        [item.value for item in project_input.dev_process_phases]
    )


def create_project(
    db: Session,
    project_input: ProjectCreateInput,
    created_by: str,
) -> ProjectResponse:
    technologies = upsert_tech_tags(
        db,
        project_input.technologies,
    )

    project = Project(
        customer_name=project_input.customer_name,
        project_name=project_input.project_name,
        start_date=project_input.start_date.isoformat(),
        created_by=created_by,
    )

    update_project_fields(project, project_input, technologies)

    db.add(project)
    db.commit()
    db.refresh(project)

    return project_to_response(project)


def update_project(
    db: Session,
    project_id: int,
    project_input: ProjectUpdateInput,
) -> ProjectResponse | None:
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.deleted_at.is_(None),
        )
    )

    if project is None:
        return None

    technologies = upsert_tech_tags(
        db,
        project_input.technologies,
    )

    update_project_fields(project, project_input, technologies)

    db.commit()
    db.refresh(project)

    return project_to_response(project)