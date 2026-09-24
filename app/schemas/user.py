import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserAuthInput(BaseModel):
    """Dữ liệu nhận vào khi Đăng nhập"""

    email: EmailStr = Field(
        ...,
        max_length=255,
        description="ユーザーのメールアドレス",
        examples=["member@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="パスワード",
        examples=["SecurePassword123"],
    )


class UserRegisterInput(UserAuthInput):
    """Dữ liệu nhận vào khi Đăng ký. Luật mật khẩu chỉ áp dụng ở đây,
    để đăng nhập sai mật khẩu vẫn trả 401 chứ không phải 422."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="パスワード（8文字以上、大文字・小文字・数字を各1つ以上）",
        examples=["SecurePassword123"],
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("パスワードには大文字を1つ以上含めてください")
        if not re.search(r"[a-z]", value):
            raise ValueError("パスワードには小文字を1つ以上含めてください")
        if not re.search(r"[0-9]", value):
            raise ValueError("パスワードには数字を1つ以上含めてください")
        return value


class UserResponse(BaseModel):
    """Dữ liệu trả về chứa thông tin người dùng (email, role)"""

    email: EmailStr
    role: str = "member"
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Dữ liệu trả về chứa token (khớp chuẩn idToken của Mentor và chuẩn Bearer)"""

    idToken: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
