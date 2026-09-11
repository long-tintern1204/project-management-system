import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.main import app
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)
# Khởi tạo client kiểm thử của FastAPI
client = TestClient(app)


# 1. Kiểm tra Endpoint Health Check cho Frontend
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok"}


# 2. Kiểm tra hàm băm mật khẩu Bcrypt lõi
def test_password_hashing():
    password = "MySecurePassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

# 3. Kiểm tra hàm tạo JWT Token độc lập
def test_create_access_token():
    payload = {"email": "token_unit_test@example.com", "role": "admin"}
    token = create_access_token(data=payload)
    # Token sinh ra phải là chuỗi không rỗng
    assert isinstance(token, str)
    assert len(token) > 0
    # Giải mã chữ ký token bằng SECRET_KEY và ALGORITHM để kiểm tra dữ liệu thật bên trong
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    assert decoded["email"] == "token_unit_test@example.com"
    assert decoded["role"] == "admin"
    assert "exp" in decoded  # Bắt buộc phải có hạn dùng exp theo chuẩn bảo mật
    
# 3. Kiểm tra Đăng ký tài khoản (Thành công & Validate lỗi 422)
def test_register_flow():
    # Pass quá ngắn (< 8 ký tự) -> Báo lỗi validate 422
    invalid_payload = {
        "email": "short@example.com",
        "password": "short",
    }
    res_invalid = client.post("/auth/register", json=invalid_payload)
    assert res_invalid.status_code == 422

    # Đăng ký hợp lệ -> Trả về 201 Created kèm idToken
    valid_payload = {
        "email": "long_lead@example.com",
        "password": "SecurePassword123@",
    }
    res_success = client.post("/auth/register", json=valid_payload)
    assert res_success.status_code == 201
    data = res_success.json()
    assert "idToken" in data
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# 4. Kiểm tra trùng Email -> Báo 409 Conflict (Test 1 trong Doc 05)
def test_register_duplicate_conflict():
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123@",
    }
    # Đăng ký lần 1 -> 201
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 201

    # Đăng ký lại lần 2 cùng email -> 409 Conflict
    res2 = client.post("/auth/register", json=payload)
    assert res2.status_code == 409
    assert res2.json()["detail"] == "このメールアドレスは既に登録されています"


# 5. Kiểm tra Đăng nhập (Sai mật khẩu 401 & Đúng 200)
def test_login_scenarios():
    email = "user_test_login@example.com"
    password = "CorrectPassword123@"

    # Đăng ký trước
    client.post("/auth/register", json={"email": email, "password": password})

    # Sai mật khẩu -> Báo 401
    res_wrong = client.post("/auth/login", json={"email": email, "password": "WrongPassword"})
    assert res_wrong.status_code == 401
    assert res_wrong.json()["detail"] == "メールアドレスまたはパスワードが正しくありません"

    # Đúng mật khẩu -> Trả về 200 kèm token
    res_ok = client.post("/auth/login", json={"email": email, "password": password})
    assert res_ok.status_code == 200
    assert "idToken" in res_ok.json()


# 6. Kiểm tra Endpoint bảo vệ GET /auth/me (Test 2 trong Doc 05)
def test_protected_route_unauthorized():
    # 1. Không gửi token -> Bị chặn 401
    res_no_token = client.get("/auth/me")
    assert res_no_token.status_code == 401

    # 2. Gửi token dỏm/sai -> Bị chặn 401
    res_fake_token = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer fake.invalid.token"}
    )
    assert res_fake_token.status_code == 401

    # 3. Đăng ký lấy token thật -> Gửi đúng header -> Nhận 200
    email = "auth_me_test@example.com"
    reg_res = client.post("/auth/register", json={"email": email, "password": "Password123@"})
    token = reg_res.json()["access_token"]

    res_valid = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_valid.status_code == 200
    assert res_valid.json()["email"] == email
    assert res_valid.json()["role"] == "member"