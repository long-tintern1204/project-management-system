# 03. PHÂN CHIA CÔNG VIỆC CHO 3 THÀNH VIÊN (WBS) & QUY TRÌNH GIT
## Bám sát 100% Kế hoạch đào tạo 4 tuần (W09 – W12) của Mentor

**Dự án:** プロジェクト管理システム (Project Performance Management System)  
**Repository GitHub:** [https://github.com/long-tintern1204/project-management-system/tree/develop](https://github.com/long-tintern1204/project-management-system/tree/develop)  
**Phân vai (Roles) trong nhóm:**
* 👑 **Long** (Trưởng nhóm - Security, QA & Frontend Integration)
* 📊 **Khanh** (@Nguyen Van Tuan Khanh / `@khanhnvtintern` - Data / Database & Read Engine)
* 🏷️ **Tuyết** (@Nguyen Thi Tuyet - Schemas, Validation & Mutation/Tags)

---

## 👥 1. MA TRẬN PHÂN CHIA CÔNG VIỆC TỔNG QUAN (W09 – W12)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        KHANH: DATA / DATABASE & READ ENGINE                            │
│  - W09: Model projects (18 fields + 3 CSV), tech_tags, users + Migration Alembic       │
│  - W10: API GET /projects (danh sách cơ bản), GET /projects/{id} (lọc soft delete)     │
│  - W11: API GET /projects nâng cao (Search 'q', Multi-filter AND/OR, Phân trang chuẩn) │
│  - W12: Tối ưu hiệu năng Query SQL, đánh Index, Demo tìm kiếm & lọc đa điều kiện       │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
┌───────────────────────────────────────┐   ┌───────────────────────────────────────────┐
│    TUYẾT: SCHEMAS & MUTATION/TAGS     │   │       LONG: SECURITY, QA & FRONTEND       │
│ - W09: Schemas Project (18 fields,    │   │ - W09: Module Auth JWT (Register/Login),  │
│   2 Enums, Validate ngày/ongoing),    │   │   Bcrypt, Vệ sĩ 401, CORS, /health,       │
│   Schema TechTag + Test Pydantic 422  │   │   Bộ 7 Unit Test Pytest (PASS 100%)       │
│ - W10: API POST /projects, PUT /{id}, │   │ - W10: API DELETE /{id} (Soft Delete),    │
│   logic tự động upsert tech_tags      │   │   bảo vệ JWT cho CRUD, seed 15-20 dự án   │
│ - W11: API GET /tech-tags?q= autocom- │   │ - W11: Test tích hợp Frontend React UI,   │
│   plete (max 20, case-insensitive)    │   │   kiểm tra chip filter, dropdown, token   │
│ - W12: Test CRUD, validate 422 & Demo │   │ - W12: Chủ trì bộ 7 Pytest xương sống,    │
│   tạo/sửa dự án, gợi ý tag            │   │   master README, kịch bản Demo 8 bước     │
└───────────────────────────────────────┘   └───────────────────────────────────────────┘
```

---

## 📋 2. CHI TIẾT CÔNG VIỆC 3 THÀNH VIÊN THEO TỪNG TUẦN

### 🗓️ TUẦN W09: Kickoff hệ thống + Thiết lập nền tảng Database, Auth & Schemas
> **Mục tiêu chung:** Nghiên cứu kỹ tài liệu `API仕様`, chốt 10 điểm đặc tả Q&A với Mentor, dựng xong CSDL 3 bảng với migration Alembic, hoàn thiện module Auth JWT có test tự động và hoàn thành hệ thống Pydantic Schemas.

#### 1. Long (Security, QA & Frontend Integration - Trưởng nhóm)
* **Nhiệm vụ trọng tâm:** Xây dựng module bảo mật JWT, mã hóa mật khẩu, bảo vệ endpoint bằng dependency 401, mở khóa kết nối Frontend và xây dựng bộ kiểm thử Pytest.
* **Phạm vi file phụ trách:**
  * `app/core/security.py`:
    * Mã hóa băm mật khẩu bằng thuật toán **Bcrypt** (`get_password_hash`, `verify_password`).
    * Hàm tạo và giải mã JWT token thời hạn **24 giờ** (`create_access_token`, `decode_access_token`).
    * Đồng bộ chuẩn biến môi trường với Khanh: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES=1440`.
    * Dependency `get_current_user`: Trích xuất `email` và `role` từ JWT token, chặn đứng mã lỗi **`401 Unauthorized`** nếu thiếu hoặc sai/hết hạn token.
  * `app/schemas/user.py`:
    * `UserAuthInput`: Ràng buộc email hợp lệ, mật khẩu từ **8 đến 100 ký tự** (Pydantic v2).
    * `TokenResponse`: Trả về trường **`idToken`** (theo đúng đặc tả của Mentor và Frontend React) cùng `access_token` và `token_type: "bearer"`.
    * `UserResponse`: Trả về thông tin `{ email, role }`.
  * `app/api/routers/auth.py`:
    * `POST /auth/register`: Đăng ký tài khoản mới $\rightarrow$ thành công trả về **`201 Created`** kèm `idToken`; nếu trùng email trả về đúng mã **`409 Conflict`** kèm thông báo tiếng Nhật `このメールアドレスは既に登録されています`.
    * `POST /auth/login`: Đăng nhập $\rightarrow$ thành công trả về **`200 OK`** kèm `idToken`; sai thông tin trả về đúng **`401 Unauthorized`** kèm thông báo tiếng Nhật `メールアドレスまたはパスワードが正しくありません`.
    * `GET /auth/me`: Endpoint bảo mật được gác cổng bởi `Depends(get_current_user)`.
  * `app/main.py`:
    * Khởi tạo app FastAPI với tiêu đề chuẩn: `プロジェクト管理システム API`.
    * Cấu hình **CORSMiddleware** cho phép các origin Frontend React (`http://localhost:5173` và `http://127.0.0.1:5173`) kết nối xuyên suốt.
    * Bổ sung endpoint **`GET /health`** (`{"status": "ok", "db": "ok"}`) đóng vai trò Readiness Probe mở khóa màn hình Frontend React.
    * Bổ sung endpoint gốc `GET /` (`{"status": "online", "docs_url": "/docs"}`).
  * `pytest.ini` & `tests/test_auth.py`:
    * Viết trọn bộ **7 bài Unit Test** bao phủ: kết nối `/health`, băm mật khẩu Bcrypt, mã hóa JWT, đăng ký 201/422, trùng email 409, đăng nhập 200/401, bảo vệ route chặn 401.
* **Nhánh Git:** `feature/long-w9-auth-jwt-and-cors`
* **Tiêu chí nghiệm thu (DoD):** Chạy `pytest tests/test_auth.py` **PASS 7/7 (100%)**; Frontend React mở bung màn hình `/login` không bị treo modal loading.

#### 2. Khanh (Data / Database & Read Engine)
* **Nhiệm vụ trọng tâm:** Thiết kế hạ tầng CSDL, khởi tạo các Model SQLAlchemy và cấu hình migration tự động bằng Alembic.
* **Phạm vi file phụ trách:**
  * `app/core/config.py`: Quản lý biến môi trường qua Pydantic BaseSettings (`DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`).
  * `app/core/database.py`: Khởi tạo SQLAlchemy Engine, `SessionLocal`, `Base = declarative_base()`, dependency `get_db`.
  * `app/models/project.py`:
    * Khai báo bảng đơn `projects` chứa đầy đủ 18 trường spec.
    * 3 cột chuỗi lưu mảng CSV: `technologies_csv: Text`, `project_types_csv: Text`, `dev_process_phases_csv: Text`.
    * Cột xóa mềm: `deleted_at: DateTime(timezone=True), nullable=True`.
  * `app/models/tech_tag.py`:
    * Khai báo bảng `tech_tags` gồm: `id` (PK, Integer, autoincrement), `name` (VARCHAR(100), UNIQUE, NOT NULL - **phân biệt hoa thường** theo câu Q4 Mentor), `created_at` (DateTime).
  * `app/models/user.py`:
    * Khai báo bảng `users` gồm: `id` (PK), `email` (VARCHAR(255), UNIQUE, NOT NULL), `hashed_password` (VARCHAR(255), NOT NULL), `role` (VARCHAR(20), default='member'), `created_at`.
  * `app/models/__init__.py` & `alembic/`:
    * Cấu hình `alembic/env.py` nạp `target_metadata = Base.metadata` của cả 3 models.
    * Tạo migration ban đầu trong `alembic/versions/` tạo đủ 3 bảng với ràng buộc UNIQUE cho `users.email` và `tech_tags.name`.
* **Nhánh Git:** `feature/khanh-w9-database-models-and-migrations`
* **Tiêu chí nghiệm thu (DoD):** Chạy lệnh `alembic upgrade head` sinh đủ 3 bảng `projects`, `tech_tags`, `users` trong CSDL với các ràng buộc `UNIQUE` và kiểu dữ liệu chuẩn xác; kiểm tra `alembic downgrade -1` và `upgrade head` thành công.

#### 3. Tuyết (Schemas, Validation & Mutation/Tags)
* **Nhiệm vụ trọng tâm:** Thiết kế toàn bộ hệ thống Pydantic Schemas DTO đầu vào/đầu ra, chuẩn hóa 2 bộ Enum và viết test validation chặn lỗi 422.
* **Phạm vi file phụ trách:**
  * `app/schemas/project.py`:
    * Định nghĩa 2 bộ Enum chuẩn dạng chuỗi:
      * `ProjectTypeCode`: `"offshore"`, `"ses"`, `"lab"`, `"new_dev"`, `"maintenance"`.
      * `DevProcessPhaseCode`: `"requirements"`, `"design"`, `"implementation"`, `"testing"`, `"release"`, `"maintenance_ops"`.
    * `ProjectCreateInput` & `ProjectUpdateInput`:
      * Khai báo đủ 18 trường với mô tả rõ ràng.
      * Validate chéo: `end_date >= start_date` (nếu cả 2 đều có giá trị).
      * Validate `is_ongoing`: Nếu `is_ongoing == True` thì bắt buộc `end_date` phải là `None`/rỗng (nếu client gửi kèm ngày kết thúc $\rightarrow$ ném lỗi **`422 Unprocessable Entity`**).
      * Validate `total_man_month >= 0` (đơn vị nhân-tháng, số thực $\ge 0$).
      * Validate `team_size >= 1` (số nguyên $\ge 1$).
      * Cho phép nhận mảng rỗng `[]` cho `technologies`, `project_types`, `dev_process_phases` theo câu Q2 Mentor.
    * `ProjectResponse`: Serializer trả về dữ liệu hiển thị, format ngày `YYYY-MM-DD`, tag dạng mảng `List[str]`, cấu hình `model_config = ConfigDict(from_attributes=True)`.
    * `ProjectListResponse`: Chuẩn cấu trúc phân trang `{ items: List[ProjectResponse], total: int, page: int, page_size: int }`.
  * `app/schemas/tech_tag.py`:
    * `TechTagCreate`: Trường `name` (VARCHAR tối đa 100 ký tự, tự động `.strip()` khoảng trắng thừa, **giữ nguyên chữ hoa/thường** theo Q4).
    * `TechTagResponse`: Gồm `{ id: int, name: str, created_at: datetime }`.
  * `tests/test_schemas.py`:
    * Viết bài Unit Test kiểm tra Pydantic validate đúng dữ liệu chuẩn.
    * Kiểm tra bắt đúng lỗi `422` khi truyền sai Enum, sai quy tắc `end_date < start_date`, hoặc truyền `end_date` khi `is_ongoing = True`.
* **Nhánh Git:** `feature/tuyet-w9-schemas-and-enums`
* **Tiêu chí nghiệm thu (DoD):** Chạy `pytest tests/test_schemas.py` PASS 100%; Swagger UI `/docs` hiển thị đầy đủ Schemas với tài liệu rõ ràng.

---

### 🗓️ TUẦN W10: Xây dựng toàn diện bộ 5 API CRUD cho Dự án
> **Mục tiêu chung:** Hoàn thiện trọn vẹn bộ 5 API CRUD đúng 18 fields, xử lý tự động upsert `tech_tags` (phân biệt hoa thường theo Q4), xóa mềm Soft Delete và bảo vệ bằng JWT.

#### 1. Tuyết (Tạo mới & Cập nhật Dự án + Upsert TechTag)
* **Nhiệm vụ trọng tâm:** Viết hàm helper upsert tag tự động và hoàn thiện 2 API tạo mới / chỉnh sửa dự án.
* **Phạm vi thực hiện:**
  * Viết hàm helper `upsert_tech_tags()` trong `app/services/project_service.py`:
    1. Nhận danh sách tên tag từ client (ví dụ: `["React", " NodeJS ", "VueJS"]`).
    2. Chuẩn hóa khoảng trắng bằng `.strip()` và loại bỏ tag rỗng `""`.
    3. **Tuyệt đối không dùng `.lower()`**: Giữ nguyên chữ hoa/thường theo đúng câu Q4 Mentor (`'React'` và `'react'` là 2 tag riêng biệt).
    4. Loại bỏ tag trùng lặp trong cùng 1 request (deduplicate).
    5. Tìm tag đã tồn tại trong DB, tự động thêm tag mới chưa có vào bảng `tech_tags`.
    6. Trả về danh sách tag chuẩn để lưu vào cột `technologies_csv` của Project.
  * Viết API `POST /projects` (tạo dự án mới):
    * Lấy email người dùng từ JWT token gán tự động vào cột `created_by`.
    * Validate dữ liệu đầu vào qua `ProjectCreateInput`.
    * Gọi helper `upsert_tech_tags()` để tự động bổ sung tag mới vào DB.
    * Lưu bản ghi mới vào CSDL và trả về `ProjectResponse` kèm status `201 Created`.
  * Viết API `PUT /projects/{id}` (cập nhật thông tin dự án):
    * Kiểm tra dự án tồn tại và chưa bị xóa mềm (`deleted_at IS NULL`), nếu không thấy trả về `404 Not Found`.
    * Cập nhật toàn diện 18 fields và gọi `upsert_tech_tags()` để đồng bộ danh sách tag mới.
* **Nhánh Git:** `feature/tuyet-w10-project-crud-and-upsert-tags`
* **Tiêu chí nghiệm thu (DoD):** Tạo dự án kèm `technologies: ["VueJS", "Docker"]`, bảng `tech_tags` tự động sinh 2 bản ghi tương ứng; chỉnh sửa dự án cập nhật chính xác 18 trường.

#### 2. Khanh (Truy vấn Danh sách & Chi tiết Dự án)
* **Nhiệm vụ trọng tâm:** Viết tầng truy vấn (Read Engine) cho danh sách dự án cơ bản và chi tiết dự án, chuyển đổi chuỗi CSV sang mảng.
* **Phạm vi thực hiện:**
  * Viết API `GET /projects` (danh sách cơ bản có phân trang):
    * Mặc định lọc bỏ các bản ghi đã xóa mềm: `WHERE deleted_at IS NULL`.
    * Sắp xếp mặc định theo `created_at DESC` (mới nhất lên đầu).
    * Chuyển đổi các cột chuỗi CSV (`technologies_csv`, `project_types_csv`, `dev_process_phases_csv`) thành mảng `List[str]`.
    * Trả về đúng định dạng bao đóng `{ items, total, page, page_size }`.
  * Viết API `GET /projects/{id}` (chi tiết dự án):
    * Truy vấn theo `id`. Nếu không thấy bản ghi hoặc dự án đã bị xóa mềm (`deleted_at IS NOT NULL`) $\rightarrow$ trả về mã **`404 Not Found`** kèm thông báo tiếng Nhật `プロジェクトが見つかりません`.
    * Trả về đầy đủ 18 fields theo schema `ProjectResponse`.
* **Nhánh Git:** `feature/khanh-w10-get-projects-and-soft-delete`
* **Tiêu chí nghiệm thu (DoD):** Gọi `GET /projects` trả về đúng cấu trúc `{ items, total, page, page_size }`; gọi `GET /projects/{id}` trả về đủ 18 fields, gọi ID không tồn tại trả về đúng `404`.

#### 3. Long (Xóa mềm Soft Delete, Bảo vệ JWT & Dữ liệu mẫu)
* **Nhiệm vụ trọng tâm:** Viết API xóa mềm, gác cổng bảo mật JWT cho toàn bộ 5 API CRUD và chuẩn bị bộ dữ liệu mẫu phong phú.
* **Phạm vi thực hiện:**
  * Viết API `DELETE /projects/{id}`:
    * Thực hiện **Soft Delete (Xóa mềm)**: Cập nhật `deleted_at = datetime.now(timezone.utc)`, tuyệt đối **không dùng lệnh DELETE vật lý trong SQL**.
    * Theo câu Q4 Mentor: Khi xóa dự án, các tag liên quan trong bảng `tech_tags` **vẫn được giữ nguyên không bị xóa theo**.
    * Trả về status `200 OK` (hoặc `204 No Content`).
  * Tích hợp Dependency `get_current_user` bảo vệ toàn bộ 5 API CRUD (`POST`, `GET`, `GET /{id}`, `PUT`, `DELETE`), yêu cầu Header `Authorization: Bearer <idToken>`.
  * Viết script `seed_data.py`: Tự động nạp sẵn **15–20 dự án mẫu** đa dạng khách hàng Nhật, tên dự án, công nghệ, trạng thái (`is_ongoing`) và thời gian để phục vụ kiểm thử và demo.
  * Viết testcase Pytest cho luồng CRUD và Soft Delete trong `tests/test_projects.py`.
* **Nhánh Git:** `feature/long-w10-delete-project-and-seed-data`
* **Tiêu chí nghiệm thu (DoD):** Sau khi gọi `DELETE /projects/{id}`, gọi lại `GET /projects` hoặc `GET /projects/{id}` không còn thấy dự án đó nữa, nhưng trong CSDL bản ghi vẫn còn và có `deleted_at`; chạy `seed_data.py` nạp thành công 15-20 dự án mẫu.

---

### 🗓️ TUẦN W11: Nâng cấp Tìm kiếm toàn văn `q`, Bộ lọc đa điều kiện, Autocomplete & Bộ Test Case Excel
> **Mục tiêu chung:** Nâng cấp API `GET /projects` (Search 'q', Multi-filter AND/OR, phân trang max 1000), API `GET /tech-tags?q=` Autocomplete, ghép nối giao diện React và **hoàn thành trọn bộ 6 sheet Test Case Excel chuẩn Nhật** theo đặc tả [`06_EXCEL_TEST_CASES_SPECIFICATION.md`](./06_EXCEL_TEST_CASES_SPECIFICATION.md).

#### 1. Khanh (Search 'q', Multi-value Filter, Pagination & Sheet 3 + Sheet 4)
* **Nhiệm vụ Backend:**
  * Tìm kiếm toàn văn qua tham số `q`: So khớp không phân biệt hoa thường (`ILIKE` hoặc `LOWER()`) trên cả 3 cột: `customer_name`, `project_name`, `description`.
  * Bộ lọc đa giá trị: `technology[]`, `project_type[]`, `dev_process_phase[]`.
  * **Quy tắc kết hợp logic chuẩn theo câu Q5 Mentor:**
    * **`OR` trong cùng 1 field**: Dự án có `React` HOẶC `NodeJS` đều được lấy.
    * **`AND` giữa các field khác nhau**: Vừa chọn `React`, vừa chọn `offshore` $\rightarrow$ Phải thỏa mãn CẢ HAI.
  * Phân trang chuẩn: Nhận `page`, `page_size` (chặn `max = 1000` theo Q6, nếu `page_size > 1000` ném lỗi **`422 Unprocessable Entity`**).
  * Đánh Index CSDL: Tạo index cho các cột hay tìm kiếm và lọc (`deleted_at`, `name` trong `tech_tags`).
* **Nhiệm vụ Test Case Excel (phụ trách 2 sheet):**
  * **Sheet 3: `プロジェクト一覧画面-UI確認`** — Kiểm tra hiển thị bảng dữ liệu, ánh xạ cột từ DB, chuyển đổi chế độ xem Table / Card, phân trang `< 1 2 3 >`, và trạng thái 0 bản ghi (0件表示: *"該当するプロジェクトが見つかりません"*).
  * **Sheet 4: `検索・フィルター機能-UI操作`** — Kiểm tra ô tìm kiếm `q`, 3 dropdown lọc đa giá trị (OR trong field, AND giữa các field), hiển thị và xóa từng chip lọc, nút xóa tất cả bộ lọc (`フィルターをクリア`).
* **Nhánh Git:** `feature/khanh-w11-filter-search-and-pagination`
* **Tiêu chí nghiệm thu (DoD):** Lọc đa điều kiện trả kết quả chính xác tuyệt đối; truyền `page_size=1001` bị chặn 422; hoàn thành 100% kết quả đánh giá (đạt `○`) cho Sheet 3 & Sheet 4.

#### 2. Tuyết (API Autocomplete Tech-tag, Chuẩn hóa quy mô & Sheet 5 + Sheet 6)
* **Nhiệm vụ Backend:**
  * Viết API `GET /tech-tags?q=`:
    * Tìm kiếm gợi ý tag **không phân biệt hoa thường (`case-insensitive`)** theo câu Q4 Mentor (`LOWER(name) LIKE LOWER(:q)`).
    * Giới hạn tối đa **20 kết quả**. Nếu `q` rỗng $\rightarrow$ trả về danh sách 20 tag mới nhất.
    * Định dạng trả về: mảng chuỗi đơn giản `List[str]` (ví dụ: `["React", "Python", "Docker"]`).
  * Chuẩn hóa validate dữ liệu quy mô dự án:
    * `total_man_month`: Đơn vị nhân-tháng (man-month, số thực $\ge 0$).
    * `team_size`: Số nguyên $\ge 1$.
  * Viết Unit test cho API Autocomplete trong `tests/test_tech_tags.py`.
* **Nhiệm vụ Test Case Excel (phụ trách 2 sheet):**
  * **Sheet 5: `プロジェクト作成画面-UI確認`** — Kiểm tra Form tạo mới 18 fields, validate bắt buộc, validate ngày tháng (`end_date >= start_date`), validate `is_ongoing=True` khóa `end_date`, tính năng gợi ý Autocomplete tag công nghệ (max 20, không phân biệt hoa thường), thêm tag mới.
  * **Sheet 6: `プロジェクト詳細・編集・削除-UI確認`** — Kiểm tra xem chi tiết 18 fields, điều hướng sang màn hình Chỉnh sửa (pre-fill dữ liệu cũ), cập nhật tag, Modal popup xác nhận Xóa mềm (nút Xóa, Hủy), kiểm tra link báo 404 khi truy cập vào dự án đã xóa.
* **Nhánh Git:** `feature/tuyet-w11-tech-tags-autocomplete`
* **Tiêu chí nghiệm thu (DoD):** Autocomplete phản hồi mượt mà; validate man-month $\ge 0$; hoàn thành 100% kết quả đánh giá (đạt `○`) cho Sheet 5 & Sheet 6.

#### 3. Long (Tích hợp Frontend React & Sheet 1 + Sheet 2)
* **Nhiệm vụ Tích hợp & QA:**
  * Khởi chạy Frontend React (`npm run dev`) kết nối tới FastAPI (`http://localhost:8000`).
  * Kiểm tra tích hợp toàn diện giao diện: debounce 300ms thanh tìm kiếm, filter chip màu, dropdown đa giá trị, nút xóa chip, nút xóa toàn bộ bộ lọc, phân trang UI, autocomplete trên Form Tạo/Sửa dự án.
  * Tinh chỉnh CORS, HTTP headers, xử lý các cảnh báo Console và lỗi mạng.
* **Nhiệm vụ Test Case Excel (phụ trách 2 sheet):**
  * **Sheet 1: `ログイン画面-UI確認`** — Kiểm tra giao diện đăng nhập `/login`, validate form, kết nối API `POST /auth/login` (200/401 tiếng Nhật), lưu trữ token JWT vào `localStorage`, link chuyển hướng sang Đăng ký.
  * **Sheet 2: `ユーザー登録画面-UI確認`** — Kiểm tra giao diện đăng ký `/register`, validate mật khẩu 8–100 ký tự và xác nhận mật khẩu, kết nối API `POST /auth/register` (201/409 trùng email), cơ chế RouteGuard chặn truy cập URL khi chưa đăng nhập, nút Đăng xuất (`ログアウト`) ở Header.
* **Nhánh Git:** `feature/long-w11-react-integration-and-ui-testing`
* **Tiêu chí nghiệm thu (DoD):** Giao diện React chạy thông suốt không lỗi Console; hoàn thành 100% kết quả đánh giá (đạt `○`) cho Sheet 1 & Sheet 2; toàn bộ file Excel Test Case được hoàn thiện đủ 6 sheet.

---

### 🗓️ TUẦN W12: Bộ Test xương sống, Tài liệu bàn giao & Báo cáo Demo
> **Mục tiêu chung:** Hoàn thiện bộ 7 bài test Pytest cốt lõi "xương sống", hoàn thiện file `README.md` chính thức hướng dẫn chạy từ A-Z, tổng duyệt kịch bản Demo 8 bước và báo cáo nghiệm thu trước Mentor.

#### 1. Long (Chủ trì Bộ Test Pytest, Master README & Kịch bản Demo)
* **Nhiệm vụ trọng tâm:** Giữ vai trò Lead QA hoàn thiện bộ kiểm thử tự động xương sống, viết tài liệu bàn giao chuẩn doanh nghiệp và xây dựng kịch bản Demo.
* **Phạm vi thực hiện:**
  * Hoàn thiện bộ **7 bài Pytest cốt lõi** theo đúng Checklist Doc 05:
    1. `test_auth_conflict_and_invalid_login`: Kiểm tra mã 409 khi trùng email và mã 401 khi sai mật khẩu.
    2. `test_unauthorized_access`: Chặn đứng mã 401 khi không có token Bearer trên các endpoint bảo vệ.
    3. `test_create_project_and_validation`: Tạo dự án đủ 18 fields, bắt lỗi 422 khi `end_date < start_date` hoặc `is_ongoing = True` kèm `end_date`.
    4. `test_tech_tags_auto_upsert`: Kiểm tra tự động upsert tag mới vào bảng `tech_tags`, giữ nguyên chữ hoa/thường theo câu Q4.
    5. `test_soft_delete_and_not_found`: Xóa mềm gán `deleted_at`, gọi lại báo 404, giữ nguyên các tag liên quan trong `tech_tags`.
    6. `test_filter_and_search_pagination`: Tìm kiếm toàn văn `q`, lọc kết hợp OR trong field và AND giữa các field, chặn `page_size > 1000` báo 422.
    7. `test_tech_tags_autocomplete`: Gợi ý tag không phân biệt hoa thường, giới hạn tối đa 20 bản ghi.
  * Viết file **`README.md`** chính thức ở thư mục gốc: Hướng dẫn cài đặt môi trường ảo Python, thiết lập file `.env`, chạy lệnh migration Alembic, nạp dữ liệu mẫu `seed_data.py`, lệnh khởi chạy server Backend & Frontend, và lệnh chạy kiểm thử `pytest`.
  * Soạn kịch bản **Demo 8 bước** chi tiết và phân công thuyết minh cho từng thành viên.
* **Nhánh Git:** `feature/long-w12-core-pytest-and-master-readme`
* **Tiêu chí nghiệm thu (DoD):** Chạy `pytest` toàn dự án báo xanh **100% PASSED**; người mới clone repo về cài đặt và chạy được hệ thống chỉ trong vòng 5 phút.

#### 2. Khanh & Tuyết (Rà soát Bug, Tối ưu & Thuyết minh Demo)
* **Khanh:**
  * Rà soát toàn bộ câu lệnh truy vấn SQL, đảm bảo không bị lỗi N+1 khi load mảng tag từ CSV.
  * Kiểm tra tính toàn vẹn dữ liệu trong DB khi xóa mềm và cập nhật dự án.
  * Chuẩn bị phần thuyết minh kỹ thuật về: Cấu trúc CSDL 3 bảng, cơ chế Soft Delete, thuật toán tìm kiếm toàn văn `q` và logic ma trận lọc OR/AND.
* **Tuyết:**
  * Rà soát toàn bộ Pydantic schemas, đảm bảo xử lý chuỗi rỗng `""` từ Frontend gửi lên thành `None`/`null`.
  * Kiểm tra lại các thông báo lỗi tiếng Nhật trên Swagger UI `/docs`.
  * Chuẩn bị phần thuyết minh kỹ thuật về: Quy tắc validate 18 fields, cơ chế tự động upsert tag và tính năng gợi ý autocomplete.

#### 3. Cả nhóm 3 người (Tổng duyệt Demo & Báo cáo Mentor)
* Cùng nhau tổng duyệt **Kịch bản Demo 8 bước** trên giao diện React thật:
  1. Đăng ký tài khoản mới $\rightarrow$ Thử đăng ký trùng báo lỗi `409 Conflict`.
  2. Đăng nhập $\rightarrow$ Nhận JWT token $\rightarrow$ Tự động chuyển hướng vào màn hình Quản lý dự án.
  3. Tạo mới dự án đủ 18 trường + thêm các tag công nghệ mới (VD: `"VueJS"`, `"Golang"`).
  4. Mở danh sách dự án: Xác nhận tag mới tự động xuất hiện trong bộ lọc $\rightarrow$ Thử tính năng Autocomplete.
  5. Thử tìm kiếm từ khóa `q` kết hợp lọc theo loại hình dự án và công nghệ (kiểm tra quan hệ OR và AND).
  6. Xem chi tiết dự án $\rightarrow$ Chỉnh sửa thông tin dự án.
  7. Bấm nút Xóa dự án (Soft delete) $\rightarrow$ Xác nhận dự án biến mất khỏi danh sách và link chi tiết báo 404.
  8. Mở Database kiểm tra: Bản ghi vẫn tồn tại, cột `deleted_at` đã được điền mốc thời gian xóa, các tag trong `tech_tags` vẫn còn nguyên.
* Trình bày báo cáo tiến độ và nghiệm thu bằng Tiếng Nhật ([`06_W09_WEEKLY_PROGRESS_REPORT_JA.md`](./06_W09_WEEKLY_PROGRESS_REPORT_JA.md)) trước Mentor.

---

## 🌿 3. QUY CHUẨN ĐẶT TÊN NHÁNH GIT & QUY TRÌNH PULL REQUEST (PR)

### 📌 1. Quy chuẩn đặt tên nhánh:
Tất cả các nhánh tính năng đều được tạo từ nhánh **`develop`** theo cú pháp chuẩn:
```text
feature/<tên_thành_viên>-w<tuần>-<tên_nhiệm_vụ>
```
* **Danh sách nhánh chuẩn 4 tuần của 3 thành viên:**
  * **Tuần W09:**
    * Long: `feature/long-w9-auth-jwt-and-cors`
    * Khanh: `feature/khanh-w9-database-models-and-migrations`
    * Tuyết: `feature/tuyet-w9-schemas-and-enums`
  * **Tuần W10:**
    * Tuyết: `feature/tuyet-w10-project-crud-and-upsert-tags`
    * Khanh: `feature/khanh-w10-get-projects-and-soft-delete`
    * Long: `feature/long-w10-delete-project-and-seed-data`
  * **Tuần W11:**
    * Khanh: `feature/khanh-w11-filter-search-and-pagination`
    * Tuyết: `feature/tuyet-w11-tech-tags-autocomplete`
    * Long: `feature/long-w11-react-integration-and-ui-testing`
  * **Tuần W12:**
    * Long: `feature/long-w12-core-pytest-and-master-readme`
    * Khanh: `feature/khanh-w12-sql-optimization-and-demo-prep`
    * Tuyết: `feature/tuyet-w12-schema-validation-and-demo-prep`

### 🔄 2. Quy trình Code Review & Merge:
1. **Quy tắc 1 nhánh = 1 nhiệm vụ:** Mỗi thành viên chỉ chỉnh sửa các file thuộc phạm vi task của mình, không sửa file chéo để tránh conflict.
2. **Kiểm tra bắt buộc trước khi tạo PR:**
   * Code chạy không có lỗi cú pháp (Syntax / Import error).
   * Chạy lệnh kiểm thử Pytest liên quan đạt kết quả **PASS 100%**.
   * Chỉ stage đúng các file code thuộc task của mình: `git add app/ tests/ ...` (loại bỏ các file tạm, file `.env`, file cấu hình không liên quan).
3. **Tạo Pull Request trên GitHub:**
   * Target branch luôn là **`develop`** (tuyệt đối không tạo PR thẳng vào `main`).
   * Gắn tag 2 thành viên còn lại vào mục **Reviewers** (@khanhnvtintern, @Nguyen Thi Tuyet, @long-tintern1204).
   * Viết mô tả PR rõ ràng gồm: Tóm tắt công việc đã làm, danh sách file thay đổi, hướng dẫn lệnh kiểm thử nhanh.
4. **Quy tắc Phê duyệt (Approval):**
   * Phải có tối thiểu **1–2 lượt Approve** từ đồng đội mới được phép merge.
   * **Trưởng nhóm (Long)** chịu trách nhiệm kiểm tra tổng thể và thực hiện merge nhánh `develop` vào `main` vào cuối mỗi tuần sau khi cả nhóm đã test tích hợp thành công.
