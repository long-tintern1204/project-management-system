import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # giúp đọc header Authorization
from jose import JWTError, jwt # mã hóa và giai mã token JWT
from passlib.context import CryptContext # giúp băm mật khóa và kiểm tra mật khẩu an toàn


# 1. Cấu hình bảo mật
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-local-env")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 1440))
ACCESS_TOKEN_EXPIRE_HOURS = JWT_EXPIRE_MINUTES / 60  # 1440 phút = 24 giờ

# 2. Cấu hình băm mật khẩu bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 3. Cấu hình đọc Bearer Token từ header Authorization
security_bearer = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """So khớp mật khẩu nhập vào với mật khẩu đã băm trong DB"""
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    """Băm mật khẩu trước khi lưu vào Database"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Tạo JWT Token có thời hạn 24 giờ và chứa payload {email, role}"""
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))    
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> dict:
    """
    Dependency bảo vệ Endpoint:
    - Nếu không có Header Authorization -> Báo lỗi 401 Unauthorized
    - Nếu token sai / hết hạn -> Báo lỗi 401 Unauthorized
    - Nếu hợp lệ -> Trả về dict user {email, role}
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証されていません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("email")
        role: str = payload.get("role", "member")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なトークンペイロードです",
            )        
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンが無効または期限切れです",
            headers={"WWW-Authenticate": "Bearer"},
        )