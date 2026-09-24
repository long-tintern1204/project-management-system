from datetime import datetime, timedelta

from app.models.tech_tag import TechTag


def seed_tags(db, names: list[str]) -> None:
    start = datetime(2026, 9, 24)

    for index, name in enumerate(names):
        db.add(
            TechTag(
                name=name,
                created_at=start + timedelta(seconds=index),
            )
        )

    db.commit()


def test_autocomplete_is_case_insensitive(
    client,
    db,
    auth_headers,
):
    seed_tags(db, ["React", "react", "React Native", "Python"])

    response = client.get(
        "/tech-tags",
        params={"q": "REACT"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == ["React Native", "react", "React"]


def test_autocomplete_returns_at_most_twenty_tags(
    client,
    db,
    auth_headers,
):
    names = [f"Python-{number:02d}" for number in range(25)]
    seed_tags(db, names)

    response = client.get(
        "/tech-tags",
        params={"q": "python"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == list(reversed(names))[:20]


def test_autocomplete_empty_query_returns_latest_tags(
    client,
    db,
    auth_headers,
):
    names = [f"Tag-{number:02d}" for number in range(25)]
    seed_tags(db, names)

    response = client.get(
        "/tech-tags",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == list(reversed(names))[:20]


def test_autocomplete_requires_token(client):
    response = client.get("/tech-tags")

    assert response.status_code == 401