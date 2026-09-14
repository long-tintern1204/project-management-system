from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.user import UserAuthInput, TokenResponse, UserResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# Lưu trữ tạm trong bộ nhớ (In-memory DB) cho tuần W09
USERS_DB = {}


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新規ユーザー登録",
)
def register(user_input: UserAuthInput):
    # 1. Kiểm tra nếu email đã tồn tại -> Báo 409 Conflict
    if user_input.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="このメールアドレスは既に登録されています",
        )

    # 2. Băm mật khẩu và lưu người dùng mới (role mặc định: member)
    hashed_pwd = get_password_hash(user_input.password)
    user_data = {
        "email": user_input.email,
        "password_hash": hashed_pwd,
        "role": "member",
    }
    USERS_DB[user_input.email] = user_data

    # 3. Tạo token trả về để Frontend tự động đăng nhập
    token = create_access_token(data={"email": user_input.email, "role": "member"})
    return {
        "idToken": token,
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="ログイン",
)
def login(user_input: UserAuthInput):
    # 1. Tìm user theo email trong bộ nhớ
    user = USERS_DB.get(user_input.email)

    # 2. Nếu không tìm thấy hoặc sai mật khẩu -> Báo 401 Unauthorized
    if not user or not verify_password(user_input.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    # 3. Mật khẩu đúng -> Tạo token 24h trả về
    token = create_access_token(data={"email": user["email"], "role": user["role"]})
    return {
        "idToken": token,
        "access_token": token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="ログイン中ユーザー情報取得",
)
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Endpoint bảo vệ:
    - Nếu không truyền Authorization Bearer token -> FastAPI trả về 401 Unauthorized
    - Nếu token đúng -> Trả về payload {email, role}
    """
    return current_user