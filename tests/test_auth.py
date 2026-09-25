import pytest
from jose import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)


# 1. Kiểm tra Endpoint Health Check cho Frontend
def test_health_check(client):
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
def test_register_flow(client):
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
def test_register_duplicate_conflict(client):
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
def test_login_scenarios(client):
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
def test_protected_route_unauthorized(client):
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

# --- Bổ sung: luật mật khẩu theo spec ---


def test_register_requires_uppercase(client):
    res = client.post("/auth/register", json={"email": "nocap@example.com", "password": "password123"})
    assert res.status_code == 422


def test_register_requires_lowercase(client):
    res = client.post("/auth/register", json={"email": "nolower@example.com", "password": "PASSWORD123"})
    assert res.status_code == 422


def test_register_requires_digit(client):
    res = client.post("/auth/register", json={"email": "nodigit@example.com", "password": "PasswordOnly"})
    assert res.status_code == 422


def test_login_with_weak_password_is_401_not_422(client):
    """Đăng nhập sai phải trả 401, không được để validator mật khẩu biến thành 422"""
    client.post("/auth/register", json={"email": "weaklogin@example.com", "password": "Password123"})
    res = client.post("/auth/login", json={"email": "weaklogin@example.com", "password": "alllowercase"})
    assert res.status_code == 401


# --- Bổ sung: response chứa object user theo sheet API詳細 ---


def test_register_response_contains_user(client):
    res = client.post("/auth/register", json={"email": "shape@example.com", "password": "Password123"})
    body = res.json()
    assert body["user"] == {"email": "shape@example.com", "role": "member"}


def test_login_response_contains_user(client):
    client.post("/auth/register", json={"email": "shape2@example.com", "password": "Password123"})
    body = client.post("/auth/login", json={"email": "shape2@example.com", "password": "Password123"}).json()
    assert body["user"] == {"email": "shape2@example.com", "role": "member"}


def test_role_is_always_member(client):
    """Client gửi role khác cũng bị bỏ qua"""
    res = client.post(
        "/auth/register",
        json={"email": "fakerole@example.com", "password": "Password123", "role": "admin"},
    )
    assert res.json()["user"]["role"] == "member"


# --- Bổ sung: user thực sự được lưu vào bảng users ---


def test_user_is_persisted_in_database(client, db):
    from app.models import User

    client.post("/auth/register", json={"email": "persist@example.com", "password": "Password123"})

    user = db.query(User).filter(User.email == "persist@example.com").one()
    assert user.role == "member"
    assert user.password_hash != "Password123"


def test_login_works_with_user_created_directly_in_db(client, db):
    """Token không còn phụ thuộc bộ nhớ tiến trình: user nằm trong DB là đăng nhập được"""
    from app.core.security import get_password_hash
    from app.models import User

    db.add(User(email="fromdb@example.com", password_hash=get_password_hash("Password123"), role="member"))
    db.commit()

    res = client.post("/auth/login", json={"email": "fromdb@example.com", "password": "Password123"})
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "fromdb@example.com"


# --- Bổ sung: health check chạm DB thật ---


def test_health_check_reports_db_ok(client):
    body = client.get("/health").json()
    assert body == {"status": "ok", "db": "ok"}
