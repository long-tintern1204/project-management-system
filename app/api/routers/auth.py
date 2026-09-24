from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import (
    TokenResponse,
    UserAuthInput,
    UserRegisterInput,
    UserResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新規ユーザー登録",
)
def register(user_input: UserRegisterInput, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_input.email, user_input.password)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="ログイン",
)
def login(user_input: UserAuthInput, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user_input.email, user_input.password)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="ログイン中ユーザー情報取得",
)
def get_me(current_user: dict = Depends(get_current_user)):
    """Thiếu token, token sai hoặc hết hạn -> 401."""
    return current_user
