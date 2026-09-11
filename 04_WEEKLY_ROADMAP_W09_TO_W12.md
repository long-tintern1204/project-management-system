# 04. LỘ TRÌNH 4 TUẦN (W09 – W12) & KẾ HOẠCH HẰNG NGÀY (DAY-BY-DAY)
## Kế hoạch chi tiết theo quy chế làm việc 3 ngày/tuần (Thứ 2 - Thứ 4 - Thứ 6)

**Dự án:** プロジェクト管理システム (Project Performance Management System)  
**Quy chế làm việc của nhóm:** Mỗi thành viên online làm việc **3 ngày / tuần** (Thứ 2, Thứ 4, Thứ 6 — tương đương 24h/tuần/người. Tổng 4 tuần = **12 ngày làm việc**).  
**Phân vai (Roles) trong nhóm:**
* 👑 **Long** (Trưởng nhóm - Security, QA & Frontend Integration)
* 📊 **Khanh** (@Nguyen Van Tuan Khanh / `@khanhnvtintern` - Data / Database & Read Engine)
* 🏷️ **Tuyết** (@Nguyen Thi Tuyet - Schemas, Validation & Mutation/Tags)

---

## 📅 1. BỨC TRANH TỔNG THỂ 4 TUẦN (12 NGÀY LÀM VIỆC)

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ W09 (Tuần 1: 3 ngày làm việc): Kickoff, Database, Auth & Schemas     (Long báo cáo tuần)│
│ - Q&A với mentor chốt 10 điểm đặc tả (18 fields, enums, soft delete, upsert tag hoa/thường) │
│ - Database: Tạo 3 model 'projects', 'tech_tags', 'users' + chạy migration Alembic       │
│ - Security: Module Auth /auth/register + /auth/login, JWT 24h, bảo vệ 401, CORS & /health│
│ - Schemas: Đủ 18 fields, 2 Enums chuẩn, validate ngày/is_ongoing, phân trang Frontend   │
│ - Kiểm thử: Bộ 7 Pytest Unit Test Auth (100% PASS), test Pydantic validation            │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼────────────────────────────────────────────┐
│ W10 (Tuần 2: 3 ngày làm việc): Toàn diện bộ 5 API CRUD Dự án         (Khanh báo cáo tuần)│
│ - CRUD Project: POST /projects, GET /projects (cơ bản), GET /{id}, PUT, DELETE          │
│ - Validate chặt chẽ 18 fields + 2 bộ enum project_types / dev_process_phases           │
│ - technologies: Tự động upsert vào tech_tags khi tạo/sửa (phân biệt hoa thường theo Q4) │
│ - DELETE: Soft delete (gán deleted_at mốc UTC, không xóa vật lý, giữ nguyên tech_tags) │
│ - Seed Data: Script seed_data.py nạp sẵn 15-20 dự án mẫu phục vụ test & demo            │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼────────────────────────────────────────────┐
│ W11 (Tuần 3: 3 ngày làm việc): Filter, Autocomplete & Test Case Excel(Tuyết báo cáo tuần)│
│ - Tìm kiếm toàn văn 'q' trên cả 3 cột customer_name, project_name, description          │
│ - Bộ lọc đa giá trị: OR trong cùng 1 field, AND giữa các field khác nhau (theo Q5)      │
│ - Phân trang chuẩn: page, page_size (giới hạn max = 1000 theo Q6), total, items        │
│ - GET /tech-tags?q=: Autocomplete tag không phân biệt hoa thường, giới hạn max 20       │
│ - Tích hợp toàn diện với Frontend React: Chip lọc, dropdown, search bar, phân trang UI  │
│ - Hoàn thành 6 Sheet Test Case Excel chuẩn Nhật chia đều 3 người (Doc 06 - 100% Pass)   │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼────────────────────────────────────────────┐
│ W12 (Tuần 4: 3 ngày làm việc): Test xương sống, README & Demo        (Cả 3 báo cáo & demo)│
│ - Bộ 7 Pytest cốt lõi "xương sống" bao phủ toàn bộ luồng Auth, CRUD, Filter, Soft delete│
│ - Tối ưu hiệu năng truy vấn SQL, đánh Index các cột tìm kiếm và lọc dữ liệu             │
│ - README.md hoàn chỉnh ở root hướng dẫn chạy dự án từ A-Z (setup trong 5 phút)          │
│ - Tổng duyệt kịch bản Demo 8 bước và thuyết minh báo cáo tiếng Nhật trước Mentor        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗓️ 2. KẾ HOẠCH CHI TIẾT TUẦN 1 (W09: Kickoff, Database, Auth & Schemas)
**Lịch làm việc:** 3 ngày (Thứ 2, Thứ 4, Thứ 6) — 8h/ngày  
**Người đại diện báo cáo tuần W09:** 👑 **Long (Trưởng nhóm)**

| Buổi làm việc | Mục tiêu chính | Long (Security, QA & Frontend) | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Kickoff & Chốt đặc tả với Mentor** | - Soạn bảng 10 câu hỏi Q&A gửi Mentor.<br>- Chốt 10 điểm đặc tả quan trọng (18 fields, soft delete, JWT 24h, tag hoa/thường, max 1000 page_size). | - Nghiên cứu sheet `データモデル`, phân tích cấu trúc 3 bảng `projects`, `tech_tags`, `users`.<br>- Khởi tạo `app/core/config.py` và kết nối DB `app/core/database.py`. | - Nghiên cứu sheet `API詳細`, phân tích 18 trường và 2 bộ Enum của Project.<br>- Định nghĩa `ProjectTypeCode` và `DevProcessPhaseCode` trong `app/schemas/project.py`. | Bản Checklist 10 câu Q&A Mentor hoàn tất ([`00_SPEC_QA_CHECKLIST_MENTOR.md`](./00_SPEC_QA_CHECKLIST_MENTOR.md)). |
| **Thứ 4 (Day 2)** | **Phát triển Core Models, Schemas & Security** | - Viết `app/core/security.py`: Băm Bcrypt, tạo JWT 24h, dependency `get_current_user` chặn 401.<br>- Viết `app/schemas/user.py` (`UserAuthInput`, `TokenResponse`, `UserResponse`).<br>- Viết `app/api/routers/auth.py` (`/register`, `/login`, `/me`). | - Viết 3 SQLAlchemy Models: `Project` (18 fields + 3 cột CSV + `deleted_at`), `TechTag` (name UNIQUE), `User` (email UNIQUE).<br>- Cấu hình `alembic/env.py` nạp `Base.metadata`. | - Viết `ProjectCreateInput`, `ProjectUpdateInput` (validate ngày kết thúc $\ge$ ngày bắt đầu, `is_ongoing = True` khóa `end_date` $\rightarrow$ lỗi 422, `total_man_month \ge 0`).<br>- Viết `TechTagCreate` và `TechTagResponse`. | Migration Alembic sinh đủ 3 bảng; Swagger UI `/docs` hiển thị đủ Auth API và Schemas. |
| **Thứ 6 (Day 3)** | **Tích hợp CORS, Unit Test & Báo cáo tuần** | - Cấu hình `app/main.py`: CORS Middleware (`localhost:5173`), `GET /health` (`status: ok, db: ok`), `GET /`.<br>- Viết trọn bộ **7 bài Unit Test** trong `tests/test_auth.py` và cấu hình `pytest.ini`.<br>- **Long đại diện báo cáo tuần W09 tiếng Nhật**. | - Chạy `alembic upgrade head` test tạo bảng thật trong DB, kiểm tra ràng buộc UNIQUE.<br>- Viết script test kết nối DB `tests/test_database.py`.<br>- Review PR của Long & Tuyết. | - Viết `ProjectListResponse` chuẩn phân trang cho React.<br>- Viết Unit Test `tests/test_schemas.py` kiểm tra bắt lỗi 422 khi sai Enum hoặc sai ngày tháng.<br>- Review PR của Long & Khanh. | Chạy `pytest tests/test_auth.py` **PASS 7/7 (100%)**; Frontend React mở bung màn hình `/login`; **3 PRs merge vào `develop`**. |

---

## 🗓️ 3. KẾ HOẠCH CHI TIẾT TUẦN 2 (W10: Xây dựng toàn diện CRUD Project)
**Lịch làm việc:** 3 ngày (Thứ 2, Thứ 4, Thứ 6) — 8h/ngày  
**Người đại diện báo cáo tuần W10:** 📊 **Khanh (Data / Read Engine)**

| Buổi làm việc | Mục tiêu chính | Long (Security, QA & Frontend) | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Khởi động tuần & Setup Layer** | - Tạo nhánh `feature/long-w10-delete-project-and-seed-data`.<br>- Viết hàm kiểm tra token bảo vệ cho toàn bộ router `/projects`.<br>- Chuẩn bị kịch bản test Soft Delete và Upsert Tag. | - Tạo nhánh `feature/khanh-w10-get-projects-and-soft-delete`.<br>- Dựng cấu trúc Service đọc dữ liệu `app/services/project_query_service.py`. | - Tạo nhánh `feature/tuyet-w10-project-crud-and-upsert-tags`.<br>- Rà soát lại Schemas `ProjectCreateInput` và `ProjectResponse`. | Thống nhất API contracts và schema đầu vào/đầu ra giữa 3 người. |
| **Thứ 4 (Day 2)** | **Auto-upsert Tag, CRUD APIs & Soft Delete** | - Viết API `DELETE /projects/{id}`: Soft Delete gán `deleted_at` UTC, không xóa vật lý, giữ nguyên tag theo Q4 Mentor.<br>- Bắt đầu viết file nạp dữ liệu mẫu `seed_data.py`. | - Viết hàm truy vấn `get_by_id()`: Bắt buộc lọc `WHERE deleted_at IS NULL` (báo `404 Not Found` nếu không tìm thấy hoặc đã xóa mềm).<br>- Viết API `GET /projects` cơ bản. | - Viết hàm helper `upsert_tech_tags()`: Xóa khoảng trắng `.strip()`, loại bỏ tag rỗng, giữ nguyên chữ hoa/thường theo Q4 Mentor.<br>- Viết API `POST /projects` (lấy email từ JWT, auto-upsert tag). | Chạy thử upsert tag: Thêm `"VueJS"` và `"vuejs"` được 2 tag riêng biệt; gọi `DELETE` ghi nhận đúng `deleted_at`. |
| **Thứ 6 (Day 3)** | **Hoàn thiện 5 API CRUD, Seed Data & Báo cáo tuần** | - Hoàn thiện `seed_data.py` nạp 15–20 dự án mẫu phong phú.<br>- Viết 3 testcase Pytest CRUD trong `tests/test_projects.py`.<br>- Cùng nhóm bật React UI kiểm tra nút Xóa (mở Modal xóa mềm). | - Hoàn thiện API `GET /projects` (phân trang, unpack CSV sang `List[str]`).<br>- Hoàn thiện API `GET /projects/{id}`.<br>- **Khanh đại diện báo cáo tuần W10 tiếng Nhật**. | - Hoàn thiện API `PUT /projects/{id}`: Cập nhật 18 fields và đồng bộ lại tag.<br>- Kiểm tra Form Tạo/Sửa trên React gửi đúng 18 fields và cập nhật tag.<br>- Review PRs và merge vào `develop`. | Đủ bộ 5 API CRUD chạy mượt mà trên Swagger UI; Frontend React thao tác CRUD trơn tru; **3 PRs merge vào `develop`**. |

---

## 🗓️ 4. KẾ HOẠCH CHI TIẾT TUẦN 3 (W11: Tìm kiếm 'q', Filter, Autocomplete & Test Case Excel)
**Lịch làm việc:** 3 ngày (Thứ 2, Thứ 4, Thứ 6) — 8h/ngày  
**Người đại diện báo cáo tuần W11:** 🏷️ **Tuyết (Schemas, Validation & Mutation/Tags)**

| Buổi làm việc | Mục tiêu chính | Long (Security, QA & Frontend) | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Phân tích Thuật toán Lọc & Autocomplete** | - Tạo nhánh `feature/long-w11-react-integration-and-ui-testing`.<br>- Rà soát tham số Query params đảm bảo yêu cầu JWT token.<br>- Chuẩn bị kịch bản test tích hợp React UI. | - Tạo nhánh `feature/khanh-w11-filter-search-and-pagination`.<br>- Thiết kế Query Builder: Xử lý logic lọc phức tạp (OR trong từng field, AND giữa các field theo Q5 Mentor). | - Tạo nhánh `feature/tuyet-w11-tech-tags-autocomplete`.<br>- Thiết kế hàm tìm kiếm tag: `大文字小文字区別なし` (không phân biệt hoa thường theo Q4 Mentor), giới hạn tối đa 20 bản ghi. | Thống nhất định dạng tham số: `technology[]`, `project_type[]`, `dev_process_phase[]`, `q`. |
| **Thứ 4 (Day 2)** | **Hoàn thiện Backend & Chuẩn bị Test Case Excel** | - Ghép nối React UI: debounce 300ms tìm kiếm `q`, filter chip màu, dropdown đa giá trị.<br>- Viết kịch bản test vào file Excel cho **Sheet 1 (`/login`)** và **Sheet 2 (`/register`, RouteGuard, Logout)** theo [`06_EXCEL_TEST_CASES_SPECIFICATION.md`](./06_EXCEL_TEST_CASES_SPECIFICATION.md). | - Triển khai tìm kiếm toàn văn `q` trên 3 cột (`customer_name`, `project_name`, `description`).<br>- Hoàn thiện logic lọc AND/OR và phân trang (chặn `page_size > 1000` ném lỗi 422).<br>- Viết kịch bản test vào file Excel cho **Sheet 3 (Danh sách `/projects`)** và **Sheet 4 (Search `q` & Filter)**. | - Hoàn thiện API `GET /tech-tags?q=`: Gợi ý tag không phân biệt hoa thường, max 20 kết quả.<br>- Chuẩn hóa validate `total_man_month` $\ge 0$ và `team_size` $\ge 1$.<br>- Viết kịch bản test vào file Excel cho **Sheet 5 (Tạo mới & Autocomplete)** và **Sheet 6 (Chi tiết, Sửa & Xóa mềm)**. | API Search/Filter/Autocomplete chạy mượt mà; Cả 3 thành viên hoàn tất soạn kịch bản cho trọn bộ 6 sheet Test Case Excel. |
| **Thứ 6 (Day 3)** | **Chạy Test Case trên UI & Báo cáo tuần** | - Chạy kiểm thử thực tế trên trình duyệt Chrome/Edge cho **Sheet 1 & Sheet 2**, đánh dấu kết quả `○`/`×`.<br>- Kiểm tra tổng thể UI không còn lỗi Console.<br>- **Long merge `develop` vào `main`**. | - Đánh Index CSDL (`idx_tech_tags_name_lower`, `idx_projects_deleted_at`).<br>- Chạy kiểm thử thực tế trên trình duyệt cho **Sheet 3 & Sheet 4**, đánh dấu kết quả `○`/`×`. | - Chạy kiểm thử thực tế trên giao diện Form thật cho **Sheet 5 & Sheet 6**, đánh dấu kết quả `○`/`×`.<br>- **Tuyết đại diện báo cáo tuần W11 tiếng Nhật**. | Toàn bộ 6 sheet Test Case trên Excel đạt **100% ○ (Pass)**; Giao diện React chạy trơn tru; Tuyết báo cáo tuần W11 thành công. |

---

## 🗓️ 5. KẾ HOẠCH CHI TIẾT TUẦN 4 (W12: Bộ Test xương sống, Master README & Nghiệm thu Demo)
**Lịch làm việc:** 3 ngày (Thứ 2, Thứ 4, Thứ 6) — 8h/ngày  
**Người đại diện báo cáo tuần W12:** 👑📊🏷️ **Cả 3 thành viên cùng báo cáo & Demo**

| Buổi làm việc | Mục tiêu chính | Long (Security, QA & Frontend) | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Bộ 7 Pytest Xương sống & Tối ưu hóa** | - **Long chủ trì**: Hoàn thiện trọn bộ **7 bài Pytest cốt lõi** trong `tests/` bao phủ 100% nghiệp vụ (Auth, CRUD 18 fields, Soft delete 404, Upsert tag hoa/thường, Filter OR/AND, Page_size > 1000, Autocomplete max 20). | - Rà soát tối ưu hóa toàn bộ câu lệnh truy vấn SQL, đảm bảo không bị lỗi N+1 queries khi load mảng tag từ CSV.<br>- Hỗ trợ dữ liệu test fixture trong `tests/conftest.py`. | - Rà soát toàn bộ Pydantic schemas, đảm bảo xử lý chuỗi rỗng `""` thành `None`/`null` từ Form React.<br>- Kiểm tra lại thông báo lỗi tiếng Nhật trên Swagger UI. | Chạy lệnh `pytest` toàn dự án báo xanh **100% PASSED**; CSDL và API đạt chuẩn tối ưu. |
| **Thứ 4 (Day 2)** | **Master README & Kịch bản Demo 8 bước** | - **Long chủ trì**: Viết file `README.md` chính ở thư mục gốc (hướng dẫn cài đặt A-Z trong 5 phút).<br>- Soạn chi tiết kịch bản Demo 8 bước và phân công thuyết minh cho từng người. | - Clone repo vào máy sạch thử nghiệm cài đặt và chạy thử hệ thống theo đúng `README.md`.<br>- Chuẩn bị phần thuyết minh kỹ thuật về CSDL và tính năng tìm kiếm/lọc. | - Kiểm tra chéo quy trình cài đặt theo `README.md`.<br>- Chuẩn bị phần thuyết minh kỹ thuật về Form 18 fields, upsert tag và autocomplete. | Người lạ clone repo về có thể cài đặt và khởi động hệ thống thành công chỉ trong vòng 5 phút; Kịch bản Demo hoàn tất. |
| **Thứ 6 (Day 3)** | **Tổng duyệt Demo, Nghiệm thu Mentor & Retro** | - Cùng nhau diễn tập trơn tru **Kịch bản Demo 8 bước** trên giao diện React thật.<br>- **Cả 3 thành viên cùng tham gia buổi Demo nghiệm thu chính thức với Mentor**.<br>- Trình bày báo cáo tiến độ và tổng kết dự án bằng Tiếng Nhật ([`06_W09_WEEKLY_PROGRESS_REPORT_JA.md`](./06_W09_WEEKLY_PROGRESS_REPORT_JA.md)).<br>- Nộp file Excel Test Case 6 Sheet (`06`) và File Excel Lịch trình (`プロジェクト管理システム_スケジュール.xlsx`).<br>- Họp Retrospective nội bộ nhóm để tổng kết khóa thực tập. | **Dự án được Mentor nghiệm thu thành công 100%**; Cả 3 thành viên hoàn thành xuất sắc kỳ thực tập. |

---

## 🎯 6. BẢNG TỔNG KẾT CAM KẾT CHUẨN ĐẦU RA 4 TUẦN (DELIVERABLES)

| Hạng mục | Tuần hoàn thành | Tổng công (h) | Thành viên sở hữu chính | Tiêu chí nghiệm thu (DoD) |
| :--- | :---: | :---: | :--- | :--- |
| **Module Auth & Security** | W09 | 24h | 👑 Long | JWT hạn 24h, Bcrypt, vệ sĩ 401, CORS, 7 Pytest PASS 100%. |
| **Database & Migrations** | W09 | 24h | 📊 Khanh | CSDL có đủ 3 bảng `projects`, `tech_tags`, `users`, chạy Alembic mượt mà. |
| **Pydantic Schemas & Enums** | W09 | 24h | 🏷️ Tuyết | Đủ 18 trường, 2 bộ Enum chuẩn, validate ngày/is_ongoing, test Pydantic PASS. |
| **Bộ 5 API CRUD Dự án** | W10 | 48h | Cả 3 thành viên | Đủ 5 API CRUD, tự động upsert tech_tags (phân biệt hoa thường), xóa mềm soft delete. |
| **Seed Data (15–20 dự án)** | W10 | 24h | 👑 Long | Script nạp sẵn dữ liệu phong phú phục vụ test và demo. |
| **Tìm kiếm 'q' & Multi-filter** | W11 | 24h | 📊 Khanh | Tìm kiếm trên 3 cột, lọc đa giá trị chuẩn OR trong field / AND giữa các field, phân trang max 1000. |
| **Autocomplete TechTag** | W11 | 24h | 🏷️ Tuyết | Gợi ý tag không phân biệt hoa thường, giới hạn tối đa 20 kết quả. |
| **Tích hợp Frontend React** | W11 | 24h | 👑 Long | Toàn bộ giao diện React (Login, List, Create, Edit, Delete, Filter, Search) kết nối thông suốt. |
| **Bộ 6 Sheet Test Case Excel** | W11 | 24h | Cả 3 thành viên | Hoàn thành kịch bản và chạy kiểm thử 6 sheet trên giao diện thật theo Doc 06, đạt 100% ○ (Pass). |
| **File Excel スケジュール (Gantt)** | W11 | 8h | Cả 3 thành viên | File Excel lịch trình 4 tuần x 3 ngày/tuần chuyên nghiệp theo chuẩn Nhật. |
| **Bộ 7 Pytest Xương sống** | W12 | 24h | 👑 Long (chủ trì) | Bao phủ toàn bộ các luồng nghiệp vụ theo đúng Checklist Doc 05, test tự động PASS 100%. |
| **Tài liệu bàn giao Master README** | W12 | 16h | 👑 Long | Hướng dẫn cài đặt và chạy dự án từ A-Z, người mới setup xong trong 5 phút. |
| **Demo 8 bước & Báo cáo tiếng Nhật** | W12 | 24h | Cả 3 thành viên | Trình diễn trơn tru toàn bộ luồng nghiệp vụ trước Mentor, nghiệm thu xuất sắc. |
| **TỔNG CỘNG TOÀN DỰ ÁN** | **4 Tuần** | **288h** | **Team 3 người** | **12 ngày làm việc / người (3 ngày/tuần x 8h = 96h/người). Hoàn thành 100%.** |
