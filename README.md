# HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT PERFORMANCE TRACKING)
## Tài Liệu Hướng Dẫn Kỹ Thuật & Kế Hoạch Triển Khai Cho Team 3 Người

---

## 📌 1. Giới thiệu tổng quan

Dự án **プロジェクト管理システム (Project Performance Management System)** là hệ thống quản lý và theo dõi thông tin, năng lực thực hiện các dự án phần mềm của công ty. 
* **Frontend**: React + TypeScript + Vite (đã có sẵn trong thư mục `InternTraining-Project-Tracking/`). Giao diện sử dụng tiếng Nhật theo chuẩn tài liệu doanh nghiệp.
* **Backend**: Xây dựng bằng **Python FastAPI**, sử dụng **SQLAlchemy**, **Pydantic v2**, hệ thống cơ sở dữ liệu (SQLite/PostgreSQL), và xác thực thông qua **JWT Bearer Token**.
* **Thành viên nhóm**:
  * **Long** (Security, QA & Frontend)
  * **Khanh** (@Nguyen Van Tuan Khanh - Data / Read Engine)
  * **Tuyết** (@Nguyen Thi Tuyet - Schemas & Mutation/Tags)

---

## 📚 2. Mục lục bộ tài liệu trong thư mục `docs/`

Để team dễ đọc hiểu, phân công và thực hiện chính xác theo lộ trình 4 tuần (W09 – W12), toàn bộ tài liệu được chia nhỏ thành các file chuyên biệt sau:

| Tên File | Nội dung chính |
| :--- | :--- |
| [**`00_SPEC_QA_CHECKLIST_MENTOR.md`**](./00_SPEC_QA_CHECKLIST_MENTOR.md) | **Kết quả Q&A chính thức với Mentor**: 10 câu hỏi & trả lời chốt toàn bộ logic nghiệp vụ (Soft delete, Upsert tag phân biệt hoa thường, validate ngày, max page_size = 1000, JWT 24h...). |
| [**`01_PROJECT_SPEC_18_FIELDS.md`**](./01_PROJECT_SPEC_18_FIELDS.md) | Đặc tả chi tiết 18 trường của Project, 2 bộ Enum chuẩn, quy tắc nghiệp vụ (Upsert `tech_tags`, Soft Delete, Quy mô man-month). |
| [**`02_BACKEND_ARCHITECTURE_AND_DB.md`**](./02_BACKEND_ARCHITECTURE_AND_DB.md) | Thiết kế Database (bảng `projects`, `tech_tags`), cấu trúc thư mục FastAPI chuẩn sử dụng **`services/`** (không dùng `crud/`), cấu hình Auth JWT & CORS. |
| [**`03_TEAM_WBS_AND_GIT_WORKFLOW.md`**](./03_TEAM_WBS_AND_GIT_WORKFLOW.md) | Phân chia công việc chi tiết cho 3 thành viên (Long, Khanh, Tuyết), quy tắc Git Branching, quy trình Review PR chống xung đột mã nguồn. |
| [**`04_WEEKLY_ROADMAP_W09_TO_W12.md`**](./04_WEEKLY_ROADMAP_W09_TO_W12.md) | Lộ trình chi tiết từng tuần theo tài liệu đào tạo: W09 (Kickoff), W10 (CRUD), W11 (Filter/Search/Paging), W12 (Testing/Docs/Demo) kèm kế hoạch ngày (Day-by-Day). |
| [**`05_TESTING_AND_FRONTEND_INTEGRATION.md`**](./05_TESTING_AND_FRONTEND_INTEGRATION.md) | Bộ kịch bản kiểm thử (Pytest xương sống), Checklist tích hợp thực tế với Frontend React và các bẫy lỗi phổ biến cần tránh. |
| [**`06_EXCEL_TEST_CASES_SPECIFICATION.md`**](./06_EXCEL_TEST_CASES_SPECIFICATION.md) | **Đặc tả 6 Sheet Test Case Excel chuẩn Nhật (Tuần W11)**: Phân chia đều cho 3 thành viên (Long: Auth; Khanh: List/Filter; Tuyết: Create/Detail/Soft Delete). |
| [**`07_BACKLOG_TEAM_GUIDELINES.md`**](./07_BACKLOG_TEAM_GUIDELINES.md) | **Quy định dự án cho Backlog**: Hướng dẫn làm việc nhóm, Git Flow, phân vai (Roles), Code conventions & DoD để copy vào Backlog task/wiki. |

---

## 🎯 3. Tóm tắt phạm vi 4 tuần đào tạo (W09 – W12)

Dựa trên tài liệu đào tạo chính thức của mentor:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ W09 (Tuần 1): Kickoff, Chốt Spec & Mô hình dữ liệu                              │
│ - Chốt 18 fields, enums, soft delete logic, upsert tech_tags                   │
│ - Tạo model DB 'projects' + 'tech_tags' + migration                             │
│ - Tích hợp Auth (/auth/register, /auth/login) kế thừa từ W06                   │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W10 (Tuần 2): Implement Project APIs (Backend) CRUD                             │
│ - CRUD Project: POST /projects, GET /projects (cơ bản), GET /{id}, PUT, DELETE │
│ - Validate 18 fields + enums project_types/dev_process_phases                  │
│ - Tự động upsert vào tech_tags khi tạo/cập nhật project                         │
│ - Soft delete (set deleted_at, loại bỏ khỏi query)                             │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W11 (Tuần 3): Filter, Search, Pagination & Autocomplete                         │
│ - GET /projects hỗ trợ multi-value filter (OR trong 1 field, AND giữa các field)│
│ - Full-text search 'q' trên customer_name, project_name, description            │
│ - Pagination chuẩn: page, page_size, total                                     │
│ - GET /tech-tags?q= Autocomplete không phân biệt hoa thường, giới hạn 20 kết quả│
│ - Chuẩn hoá total_man_month (man-month, không phải tiền) & team_size           │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W12 (Tuần 4): Test xương sống, Final Docs & Final Demo                          │
│ - Bộ 5-7 testcases Pytest (Auth, CRUD, Soft delete, Filter/Search, Tech-tags)  │
│ - README backend hoàn chỉnh + Demo kịch bản 6-8 bước                            │
│ - Nghiệm thu, Retro & Báo cáo cá nhân                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```
