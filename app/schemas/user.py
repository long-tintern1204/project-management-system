from pydantic import BaseModel, EmailStr, Field

class UserAuthInput(BaseModel):
    """Dữ liệu nhận vào khi Đăng ký / Đăng nhập"""
    email: EmailStr = Field(
        ...,
        max_length=255,
        description="ユーザーのメールアドレス）",
        examples=["member@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="パスワード（8文字以上）",
        examples=["SecurePassword123@"],
    )
    
class TokenResponse(BaseModel):
    """Dữ liệu trả về chứa token (khớp chuẩn idToken của Mentor và chuẩn Bearer)"""
    idToken: str
    access_token: str
    token_type: str = "bearer"
    

class UserResponse(BaseModel):
    """Dữ liệu trả về chúa thống tin người dùng (email, role) """
    email: EmailStr
    role: str = "member"
    model_config = {"from_attributes": True}