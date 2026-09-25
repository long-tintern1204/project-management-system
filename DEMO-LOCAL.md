# Chạy demo trên máy local

Nhánh `demo/fullstack-local` chứa **cả backend và frontend** trong một repo,
đã chỉnh sửa để chạy được ngay. Không cần clone repo nào khác.

```
project/              backend (FastAPI)  → http://localhost:8000
└── frontend/         frontend (React)   → http://localhost:5173
```

---

## 1. Lấy code

```powershell
git clone git@github.com:long-tintern1204/project-management-system.git project
cd project
git checkout demo/fullstack-local
```

---

## 2. Backend

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
```

Tạo DB và nạp dữ liệu mẫu:

```powershell
alembic upgrade head
python seed_data.py
```

Kết quả mong đợi:

```
✓ Created user: admin@gmail.com (Password: AdminPass123@, Role: member)
✓ Created user: admin@example.com (Password: Password123, Role: member)
✓ Synchronized 63 unique tech tags (added 63 new tags)
✓ Added 51 projects into database.
```

Chạy:

```powershell
uvicorn app.main:app --reload --port 8000
```

Kiểm tra http://localhost:8000/health phải trả `{"status":"ok","db":"ok"}`

---

## 3. Frontend

Mở **terminal thứ hai**:

```powershell
cd project\frontend
copy .env.example .env
npm install
npm run dev
```

Mở http://localhost:5173

> Frontend trên nhánh này đã sửa `listTechTags()` để nhận `{ items: [...] }` — backend đổi
> định dạng response ở PR #16 theo sheet `API詳細`. Bản gốc ở repo của anh Nam chưa có sửa này
> nên dropdown lọc công nghệ sẽ trống.

---

## 4. Tài khoản demo

| Email | Mật khẩu |
|---|---|
| `admin@example.com` | `Password123` |
| `admin@gmail.com` | `AdminPass123@` |

Hoặc đăng ký mới. Mật khẩu phải ≥ 8 ký tự và có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số.

---

## 5. Dữ liệu mẫu có gì

51 dự án, **mọi trường đều được điền** (riêng `end_date` để trống ở 22 dự án đang chạy
vì quy tắc `is_ongoing = true` thì `end_date` phải rỗng).

**project_type** — cả 5 giá trị đều có dữ liệu

| Giá trị | Số dự án |
|---|---|
| `new_dev` | 34 |
| `offshore` | 23 |
| `maintenance` | 17 |
| `ses` | 15 |
| `lab` | 13 |

**dev_process_phase** — cả 6 giá trị

| Giá trị | Số dự án |
|---|---|
| `implementation` | 47 |
| `design` | 43 |
| `testing` | 40 |
| `requirements` | 28 |
| `release` | 26 |
| `maintenance_ops` | 14 |

**technology** — 63 loại. Có cả `Java` (7 dự án) và `JavaScript` (2 dự án)
để kiểm chứng bộ lọc không khớp nhầm.

---

## 6. Kịch bản demo gợi ý

1. Mở http://localhost:5173 → đăng nhập `admin@example.com` / `Password123`
2. Danh sách hiện 51 dự án, phân trang 20/trang
3. Gõ `刷新` vào ô tìm kiếm → 7 kết quả
4. Lọc công nghệ `React` → 10, thêm `Vue.js` → 15 (OR trong cùng trường)
5. Giữ `React`, thêm loại `offshore` → 6 (AND giữa các trường)
6. Lọc `Java` → 7, kiểm tra không có dự án nào dùng `JavaScript` lọt vào
7. Mở chi tiết một dự án → sửa → lưu
8. Xóa một dự án → biến mất khỏi danh sách, `total` giảm 1
9. Mở lại URL chi tiết dự án vừa xóa → báo không tìm thấy (xóa mềm)

---

## 7. Chạy test

```powershell
.venv\Scripts\activate
pytest -q
```

Kết quả: **82 passed**

Kiểm tra kiểu của frontend:

```powershell
cd frontend
npx tsc -b --noEmit
```

---

## 8. Làm lại dữ liệu từ đầu

```powershell
del app.db
alembic upgrade head
python seed_data.py
```

`seed_data.py` tự bỏ qua dự án đã tồn tại (theo cặp `customer_name` + `project_name`)
nên chạy lại nhiều lần không tạo bản ghi trùng.

---

## 9. Khi gặp sự cố

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Frontend kẹt ở màn hình chờ | Backend chưa chạy | Mở `http://localhost:8000/health`, phải thấy `db: ok` |
| Đăng nhập báo lỗi mạng | CORS | Frontend phải chạy đúng cổng 5173 — `app/main.py` chỉ mở cho cổng này |
| `no such table: users` | Chưa chạy migration | `alembic upgrade head` |
| Danh sách trống | Chưa seed | `python seed_data.py` |
| Cổng bị chiếm | Tiến trình cũ còn sống | `taskkill /F /IM uvicorn.exe` hoặc `taskkill /F /IM node.exe` |
| Lọc `C#` trên Swagger ra 0 kết quả | Dấu `#` cắt URL | Gõ `C%23`. Frontend tự encode nên không dính |
| `pip install` lỗi encoding | `requirements.txt` bị ghi UTF-16 | Không dùng `pip freeze > requirements.txt` trong PowerShell |

---

## 10. Lưu ý về phạm vi tìm kiếm

`q` chỉ tìm trên **3 cột**: `customer_name`, `project_name`, `description` — đúng theo sheet `API詳細`.
Nên tìm một từ chỉ xuất hiện trong `outcome_note` (ví dụ `削減`) sẽ ra 0 kết quả. Đây là hành vi cố ý.

---

## 11. Quan hệ giữa các nhánh

| Nhánh | Nội dung | Dùng để |
|---|---|---|
| `develop` | Code chung của nhóm | Nhánh tích hợp |
| `fix/backend-demo-ready` | Backend đã sửa đầy đủ | Mở PR vào `develop` |
| `demo/fullstack-local` | `fix/backend-demo-ready` + thư mục `frontend/` | Clone về chạy demo ngay |

Nhánh `demo/fullstack-local` **không nên merge vào `develop`** vì nó chứa bản sao của
frontend. Phần backend đã nằm trong `fix/backend-demo-ready` để merge riêng.
