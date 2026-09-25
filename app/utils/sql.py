"""Hàm tiện ích dùng chung khi dựng câu truy vấn SQL."""

LIKE_ESCAPE = "\\"


def escape_like(value: str) -> str:
    """Escape ký tự đại diện của LIKE (% _) để coi chúng là ký tự tìm kiếm bình thường"""
    return (
        value.replace(LIKE_ESCAPE, LIKE_ESCAPE * 2)
        .replace("%", LIKE_ESCAPE + "%")
        .replace("_", LIKE_ESCAPE + "_")
    )
