from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User

DEFAULT_ROLE = "member"


def _token_payload(user: User) -> dict:
    """Body trả về cho register / login, khớp sheet API詳細."""
    token = create_access_token(data={"email": user.email, "role": user.role})
    return {
        "idToken": token,
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": user.email, "role": user.role},
    }


def register_user(db: Session, email: str, password: str) -> dict:
    """Tạo tài khoản mới. Email đã tồn tại -> 409."""
    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="このメールアドレスは既に登録されています",
        )

    user = User(
        email=email,
        password_hash=get_password_hash(password),
        role=DEFAULT_ROLE,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        # Hai request cùng đăng ký một email trong tích tắc
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="このメールアドレスは既に登録されています",
        ) from None

    db.refresh(user)
    return _token_payload(user)


def login_user(db: Session, email: str, password: str) -> dict:
    """Đăng nhập. Sai email hoặc sai mật khẩu đều trả cùng một thông báo 401."""
    user = db.scalar(select(User).where(User.email == email))

    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    return _token_payload(user)
