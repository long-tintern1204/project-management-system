# Chạy demo trên máy local

Hướng dẫn dựng lại **đúng môi trường demo** trên nhánh `feature/khanh-w12-auth-db-and-seed-data`:
backend cổng 8000, frontend cổng 5173, 51 dự án mẫu phủ đủ mọi bộ lọc.

Frontend nằm ở repo riêng: https://github.com/namlp721/InternTraining-Project-Tracking

Cây thư mục sau khi làm xong:

```
<thư mục làm việc>/
├── project/      backend  (repo này)             → http://localhost:8000
└── frontend/     frontend (repo của anh Nam)     → http://localhost:5173
```

---

## 1. Backend

```powershell
git clone git@github.com:long-tintern1204/project-management-system.git project
cd project
git checkout feature/khanh-w12-auth-db-and-seed-data

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

Kiểm tra: http://localhost:8000/health phải trả `{"status":"ok","db":"ok"}`

---

## 2. Frontend

```powershell
cd ..
git clone https://github.com/namlp721/InternTraining-Project-Tracking.git frontend
cd frontend
npm install
```

Tạo file `.env` trong thư mục `frontend`:

```
VITE_API_BASE_URL=http://localhost:8000
```

### Bắt buộc: áp patch tech-tags

Backend đã đổi `GET /tech-tags` sang `{ items: [...] }` theo sheet `API詳細` (PR #16),
nhưng frontend vẫn đọc mảng trần nên **dropdown lọc công nghệ sẽ trống**.

```powershell
git apply ../project/frontend-tech-tags.patch
```

Nếu anh Nam đã sửa ở repo frontend thì bỏ qua bước này (lệnh trên sẽ báo lỗi đã áp rồi).

Chạy:

```powershell
npm run dev
```

Mở http://localhost:5173

---

## 3. Tài khoản demo

| Email | Mật khẩu |
|---|---|
| `admin@example.com` | `Password123` |
| `admin@gmail.com` | `AdminPass123@` |

Hoặc đăng ký mới. Mật khẩu phải ≥ 8 ký tự và có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số.

---

## 4. Dữ liệu mẫu có gì

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

## 5. Kịch bản demo gợi ý

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

## 6. Chạy test

```powershell
cd project
.venv\Scripts\activate
pytest -q
```

Kết quả: **82 passed**

---

## 7. Làm lại dữ liệu từ đầu

```powershell
del app.db
alembic upgrade head
python seed_data.py
```

`seed_data.py` tự bỏ qua dự án đã tồn tại (theo cặp `customer_name` + `project_name`)
nên chạy lại nhiều lần không tạo bản ghi trùng.

---

## 8. Khi gặp sự cố

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Frontend kẹt ở màn hình chờ | Backend chưa chạy | Mở `http://localhost:8000/health`, phải thấy `db: ok` |
| Đăng nhập báo lỗi mạng | CORS | Frontend phải chạy đúng cổng 5173 — `app/main.py` chỉ mở cho cổng này |
| Dropdown lọc công nghệ trống | Chưa áp patch mục 2 | `git apply ../project/frontend-tech-tags.patch` |
| `no such table: users` | Chưa chạy migration | `alembic upgrade head` |
| Danh sách trống | Chưa seed | `python seed_data.py` |
| Cổng bị chiếm | Tiến trình cũ còn sống | `taskkill /F /IM uvicorn.exe` hoặc `taskkill /F /IM node.exe` |
| Lọc `C#` trên Swagger ra 0 kết quả | Dấu `#` cắt URL | Gõ `C%23`. Frontend tự encode nên không dính |
| `pip install` lỗi encoding | `requirements.txt` bị ghi UTF-16 | Không dùng `pip freeze > requirements.txt` trong PowerShell |

---

## 9. Lưu ý về phạm vi tìm kiếm

`q` chỉ tìm trên **3 cột**: `customer_name`, `project_name`, `description` — đúng theo sheet `API詳細`.
Nên tìm một từ chỉ xuất hiện trong `outcome_note` (ví dụ `削減`) sẽ ra 0 kết quả. Đây là hành vi cố ý.
