# 03. PHÂN CHIA CÔNG VIỆC CHO 3 THÀNH VIÊN (WBS) & QUY TRÌNH GIT
## Bám sát 100% Kế hoạch đào tạo 4 tuần (W09 – W12)

**Dự án:** プロジェクト管理システム (Project Performance Management System)  
**Repository GitHub:** [https://github.com/long-tintern1204/project-management-system/tree/develop](https://github.com/long-tintern1204/project-management-system/tree/develop)  
**Thành viên:** 
* **Long** (Trưởng nhóm - Security, QA & Frontend)
* **Khanh** (@Nguyen Van Tuan Khanh - Data / Read Engine)
* **Tuyết** (@Nguyen Thi Tuyet - Schemas & Mutation/Tags)

---

## 👥 1. MA TRẬN PHÂN CHIA CÔNG VIỆC (WBS) THEO TỪNG TUẦN

Toàn bộ khối lượng công việc được phân bổ chính xác theo đúng 3 cột trong bảng kế hoạch của Mentor (Scope $\rightarrow$ Deliverables $\rightarrow$ Tiêu chí nghiệm thu DoD):

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           KHANH: DATA / READ ENGINE                             │
│  - W09: Model projects (bảng đơn, 4 cột CSV/flag), bảng tech_tags + migrations   │
│  - W10: API GET /projects (list cơ bản), GET /projects/{id} (check soft delete) │
│  - W11: API GET /projects nâng cao (Search 'q', Filter multi-value, Pagination) │
│  - W12: Test query & Demo tìm kiếm, lọc dữ liệu                                 │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────────┐
│     TUYẾT: SCHEMAS & MUTATION/TAGS    │ │       LONG: SECURITY, QA & FRONTEND   │
│ - W09: Pydantic Schemas & Enums chuẩn │ │ - W09: Tích hợp Auth JWT (/auth/login,│
│ - W10: API POST /projects, PUT /{id}, │ │   /auth/register), bảo vệ endpoint 401│
│   logic tự động upsert vào tech_tags  │ │ - W10: API DELETE /{id} (Soft delete),│
│ - W11: API GET /tech-tags?q= autocom- │ │   seed data mẫu, kiểm tra merge main  │
│   plete (max 20), chuẩn hóa man-month │ │ - W11: Kiểm tra bảo vệ JWT, test UI   │
│ - W12: Test CRUD, validate 422 & Demo │ │ - W12: 5-7 Pytest cốt lõi, README cuối│
│   tạo/sửa dự án, autocomplete         │ │   + Demo 6-8 bước, handover dự án     │
└───────────────────────────────────────┘ └───────────────────────────────────────┘
```

---

## 📋 2. CHI TIẾT CÔNG VIỆC THEO TỪNG TUẦN (W09 – W12)

### 🗓️ TUẦN W09: Kickoff hệ thống quản lý 実績 + Chốt scope/backlog
> **Mục tiêu chung:** Đọc kỹ tài liệu `API仕様`, hoàn thành Q&A với mentor, dựng xong Database models + migrations, và đưa module Auth từ W06 vào chạy trên project thật.

* **Khanh (Data / Read Engine)**:
  * Đọc sheet `データモデル`, thiết lập kết nối DB (`app/core/database.py`, `app/core/config.py`).
  * Viết model `projects` dạng bảng đơn gồm: 18 trường spec + các cột chuỗi (`technologies_csv`, `project_types_csv`, `dev_process_phases_csv`) + cột `deleted_at`.
  * Viết model `tech_tags` (id, name, created_at).
  * Cấu hình Alembic và chạy migration tạo bảng trên DB.
  * **Tiêu chí xong (DoD):** Migration chạy thành công, tên cột đúng data model (KHÔNG dùng bảng Technology cũ).
* **Tuyết (Schemas & Mutation/Tags)**:
  * Viết Pydantic schemas cơ bản cho Project và TechTag (`app/schemas/project.py`, `app/schemas/tech_tag.py`).
  * Định nghĩa đúng 2 bộ Enum chuẩn: `project_types` (offshore, ses, lab, new_dev, maintenance) và `dev_process_phases` (requirements, design, implementation, testing, release, maintenance_ops).
* **Long (Security, QA & Frontend - Trưởng nhóm)**:
  * Hoàn thiện bảng Checklist Q&A chốt spec với mentor (đã chốt xong 10 câu).
  * Áp dụng module `/auth/register` và `/auth/login` (kế thừa từ tuần W06) vào project thật.
  * Thiết lập dependency `get_current_user` để mọi endpoint sau này yêu cầu token JWT hợp lệ.
  * **Tiêu chí xong (DoD):** `/auth/register` (201/409) và `/auth/login` (200/401) chạy đúng trên project thật; gọi endpoint được bảo vệ mà không có token thì trả về `401`.

---

### 🗓️ TUẦN W10: Implement Project APIs (Backend) theo đúng spec
> **Mục tiêu chung:** Hoàn thiện đầy đủ bộ 5 API CRUD cho Project đúng 18 fields, tự động upsert `tech_tags` và xóa mềm soft delete.

* **Tuyết (Schemas & Mutation/Tags)**:
  * Viết API `POST /projects` (validate field required: `customer_name`, `project_name`, validate 2 bộ enum).
  * Viết logic tự động upsert danh sách `technologies` vào bảng `tech_tags` khi tạo hoặc cập nhật dự án (so khớp phân biệt hoa thường theo Q4 Mentor).
  * Viết API `PUT /projects/{id}` (cập nhật toàn bộ thông tin dự án, đồng bộ lại tag).
* **Khanh (Data / Read Engine)**:
  * Viết API `GET /projects` (danh sách cơ bản, có phân trang, mặc định loại bỏ các bản ghi đã xóa `WHERE deleted_at IS NULL` — chưa cần filter, để dành cho W11).
  * Viết API `GET /projects/{id}` (xem chi tiết, nếu không có hoặc đã bị xóa mềm `deleted_at IS NOT NULL` $\rightarrow$ trả về `404 Not Found`).
* **Long (Security, QA & Frontend - Trưởng nhóm)**:
  * Viết API `DELETE /projects/{id}` (Soft Delete: gán `deleted_at = datetime.utcnow()`, không xóa vật lý).
  * Đảm bảo tất cả endpoint CRUD đều được bảo vệ bằng JWT (`Authorization: Bearer <token>`).
  * Viết script `seed_data.py` nạp sẵn 15-20 dự án mẫu.
  * Kiểm tra lần cuối, duyệt PR và merge vào nhánh `main` khi kết thúc tuần W10.
* **Tiêu chí nghiệm thu tuần W10 (DoD):**
  * CRUD Project chạy đúng, validate rõ ràng theo spec (`customer_name`/`project_name` required, enum đúng danh sách).
  * Endpoint được bảo vệ bởi JWT.
  * Sau khi gọi `DELETE`, gọi lại `GET /projects` hoặc `GET /projects/{id}` không còn trả record đó nữa.

---

### 🗓️ TUẦN W11: Implement filter/search + pagination + Tech-tags autocomplete
> **Mục tiêu chung:** Nâng cấp API danh sách `GET /projects` với bộ lọc đa điều kiện, tìm kiếm toàn văn `q`, phân trang chuẩn và API autocomplete cho tag.

* **Khanh (Data / Read Engine)**:
  * Nâng cấp API `GET /projects`:
    * Hỗ trợ tìm kiếm toàn văn `q` trên cả 3 cột: `customer_name`, `project_name`, `description`.
    * Bộ lọc đa giá trị: `technology[]`, `project_type[]`, `dev_process_phase[]`.
    * Logic kết hợp chuẩn: **OR trong cùng 1 field, AND giữa các field khác nhau**.
    * Phân trang chuẩn: nhận `page`, `page_size` (giới hạn `max = 1000`), trả về đủ `{ items, total, page, page_size }`.
* **Tuyết (Schemas & Mutation/Tags)**:
  * Viết API `GET /tech-tags?q=`:
    * Hỗ trợ autocomplete cho ô nhập công nghệ.
    * Tìm kiếm không phân biệt hoa thường (`case-insensitive`), giới hạn tối đa 20 kết quả, `q` rỗng trả về toàn bộ (tối đa 20).
  * Chuẩn hóa validate dữ liệu quy mô:
    * `total_man_month`: Đơn vị nhân-tháng (man-month, **KHÔNG PHẢI TIỀN**), số thực $\ge 0$.
    * `team_size`: Số nguyên $\ge 1$.
* **Long (Security, QA & Frontend - Trưởng nhóm)**:
  * Kiểm tra tính nhất quán giữa Backend với giao diện Frontend React (thanh tìm kiếm, các dropdown lọc, phân trang, chip filter).
  * Duyệt PR và merge `develop` vào `main`.
* **Tiêu chí nghiệm thu tuần W11 (DoD):**
  * Kết hợp nhiều filter cùng lúc chạy đúng (OR trong 1 field, AND giữa các field).
  * Phân trang trả đúng `total`, `page`, `page_size`.
  * `tech-tags` autocomplete đúng, case-insensitive, tối đa 20 kết quả.
  * Dữ liệu quy mô `total_man_month`/`team_size` nhất quán, validate rõ ràng.

---

### 🗓️ TUẦN W12: Tests tối thiểu + Final docs + Final demo
> **Mục tiêu chung:** Đóng gói sản phẩm, viết bộ test kiểm thử tự động, chuẩn bị tài liệu chạy dự án và tiến hành nghiệm thu Demo với Mentor.

* **Long (Security, QA & Frontend - Trưởng nhóm)**:
  * Chủ trì viết bộ **5–7 pytest tests "xương sống"** (Auth conflict 409, login fail 401, unauthorized 401, CRUD Project + validate 422/404, soft delete, filter/search, tech-tags).
  * Viết file `README.md` chính thức ở root hướng dẫn chạy backend từ A-Z.
  * Chuẩn bị kịch bản Demo 6–8 bước.
  * Kiểm tra toàn bộ codebase, chốt bản phát hành cuối cùng trên nhánh `main`.
* **Khanh (Data / Read Engine)**:
  * Fix các lỗi phát sinh liên quan đến truy vấn DB, tối ưu hóa index.
  * Phụ trách dẫn dắt và trình bày phần Demo tìm kiếm/bộ lọc trong buổi nghiệm thu.
  * Viết báo cáo cá nhân tuần W12.
* **Tuyết (Schemas & Mutation/Tags)**:
  * Fix các lỗi liên quan đến format response, validation message.
  * Hỗ trợ phần Demo tạo/chỉnh sửa dự án và gợi ý tag.
  * Viết báo cáo cá nhân tuần W12.
* **Tiêu chí nghiệm thu tuần W12 (DoD):**
  * Toàn bộ testcase Pytest pass xanh 100%.
  * Người khác clone repo, làm theo file `README.md` chạy thành công đúng theo tài liệu `API仕様` (không còn nhắc tới model Technology cũ hay Report API cũ).
  * Hoàn thành Final Demo, Retrospective và nộp báo cáo cá nhân.

---

## 🌿 3. QUY TRÌNH GIT FLOW & QUẢN LÝ MÃ NGUỒN

### 3.1. Cây phân nhánh
* **`main`**: Nhánh chính (Production). Chỉ merge khi toàn bộ task trong tuần hoàn thành và test chạy ổn định. **Long phụ trách kiểm tra lần cuối và merge vào nhánh này**.
* **`develop`**: Nhánh tích hợp chung (Base branch cho cả team). Mọi nhánh tính năng đều checkout từ đây và hợp nhất về đây.
* **`feature/...`**: Nhánh làm việc độc lập của từng dev.

### 3.2. Quy ước đặt tên nhánh
* **Định dạng:** `feature/w<số_tuần>-<tên_tính_năng>`
* **Ví dụ:**
  * W09: `feature/w9-models-and-database` (Khanh), `feature/w9-auth-jwt` (Long)
  * W10: `feature/w10-crud-project-api` (Tuyết), `feature/w10-read-apis` (Khanh), `feature/w10-soft-delete-seed` (Long)
  * W11: `feature/w11-search-filter-paging` (Khanh), `feature/w11-tech-tags-autocomplete` (Tuyết)
  * W12: `feature/w12-pytest-core` (Long)

### 3.3. Quy ước Commit (Conventional Commits)
* `feat:` Tính năng mới (VD: `feat: add soft delete logic for projects`)
* `fix:` Sửa lỗi (VD: `fix: return 404 when project is soft deleted`)
* `refactor:` Tối ưu code mà không thay đổi logic nghiệp vụ
* `test:` Thêm/sửa testcase Pytest
* `docs:` Cập nhật tài liệu hướng dẫn

> ⚠️ **Chú ý:** Tuyệt đối **KHÔNG PUSH TRỰC TIẾP** vào nhánh `develop` hoặc `main` khi chưa có Approve.

### 3.4. Quy trình Pull Request (PR)
1. Kéo code mới nhất từ `develop` về nhánh cá nhân và test local trước khi tạo PR.
2. Tạo PR vào nhánh `develop`, tag thành viên còn lại vào review.
3. Có ít nhất **1 Approve** $\rightarrow$ Người tạo PR tự bấm merge vào `develop`.

---

## 📋 4. QUẢN LÝ TASK TRÊN BACKLOG & TIÊU CHUẨN DoD
1. **Quản lý Task**:
   * Người đại diện báo cáo tuần đó chịu trách nhiệm tạo toàn bộ task WBS của tuần trên Backlog, gán hạn chót (**Start Date**, **Due Date**) và phân công cụ thể cho từng thành viên:
     * **W10:** Long tạo task & báo cáo tuần.
     * **W11:** Khanh tạo task & báo cáo tuần.
     * **W12:** Tuyết tạo task & báo cáo tuần.
   * Mỗi thành viên có trách nhiệm cập nhật trạng thái task (`In Progress` / `Resolved` / `Closed`) theo đúng tiến độ thực tế.
2. **Tiêu chuẩn hoàn thành Task (DoD)**:
   - [ ] Code tuân thủ đúng kiến trúc, bắt buộc dùng thư mục `app/services/` (không dùng `crud/`), format sạch sẽ.
   - [ ] Test thủ công trên Swagger UI hoặc Postman đạt 100% case.
   - [ ] Đã tạo Pull Request, được đồng đội Approve và merge vào `develop`.
   - [ ] Đã thêm Start Date và Due Date trên Backlog.

---

## ⏰ 5. GIAO TIẾP & BÁO CÁO HẰNG NGÀY (DAILY SYNC)
Mỗi ngày cập nhật 3 câu hỏi:
1. *Hôm nay đã làm được gì? (Tiến độ % của task hiện tại, phần nào chưa xong?)*
2. *Ngày mai dự kiến làm gì?*
3. *Có gặp khó khăn / blocker nào cần hỗ trợ hoặc thảo luận không?*
