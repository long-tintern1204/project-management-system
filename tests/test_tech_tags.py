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
    seed_tags(
        db,
        ["React", "react", "React Native", "Python"],
    )

    response = client.get(
        "/tech-tags",
        params={"q": "REACT"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["items"] == [
        "React",
        "react",
        "React Native",
    ]


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
    assert response.json()["items"] == [
        "Python-00",
        "Python-01",
        "Python-02",
        "Python-03",
        "Python-04",
        "Python-05",
        "Python-06",
        "Python-07",
        "Python-08",
        "Python-09",
        "Python-10",
        "Python-11",
        "Python-12",
        "Python-13",
        "Python-14",
        "Python-15",
        "Python-16",
        "Python-17",
        "Python-18",
        "Python-19",
    ]


def test_autocomplete_empty_query_returns_tags(
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
    assert response.json()["items"] == [
        "Tag-00",
        "Tag-01",
        "Tag-02",
        "Tag-03",
        "Tag-04",
        "Tag-05",
        "Tag-06",
        "Tag-07",
        "Tag-08",
        "Tag-09",
        "Tag-10",
        "Tag-11",
        "Tag-12",
        "Tag-13",
        "Tag-14",
        "Tag-15",
        "Tag-16",
        "Tag-17",
        "Tag-18",
        "Tag-19",
    ]


def test_autocomplete_treats_like_wildcards_as_normal_text(
    client,
    db,
    auth_headers,
):
    seed_tags(
        db,
        ["C_Sharp", "100%Pure", "JavaScript", "Java"],
    )

    response_percent = client.get(
        "/tech-tags",
        params={"q": "%"},
        headers=auth_headers,
    )
    response_underscore = client.get(
        "/tech-tags",
        params={"q": "_"},
        headers=auth_headers,
    )

    assert response_percent.status_code == 200
    assert response_percent.json()["items"] == ["100%Pure"]

    assert response_underscore.status_code == 200
    assert response_underscore.json()["items"] == ["C_Sharp"]


def test_autocomplete_requires_token(client):
    response = client.get("/tech-tags")

    assert response.status_code == 401