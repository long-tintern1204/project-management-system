# [RULE] QUY ĐỊNH DỰ ÁN, GIT FLOW & PHÂN CÔNG TRÁCH NHIỆM (W09 – W12)
## Dự án: プロジェクト管理システム (Project Performance Management System)

> **Nhóm thực hiện**: 
> * **Long** (Trưởng nhóm - Security, QA & Frontend)
> * **Khanh** (@Nguyen Van Tuan Khanh - Data / Read Engine)
> * **Tuyết** (@Nguyen Thi Tuyet - Schemas & Mutation/Tags)
> 
> **Repository GitHub**: [https://github.com/long-tintern1204/project-management-system/tree/develop](https://github.com/long-tintern1204/project-management-system/tree/develop)
>
> **Yêu cầu chung**: Toàn bộ thành viên tuân thủ nghiêm ngặt trong suốt quá trình thực hiện dự án từ tuần W09 đến W12 để đảm bảo tiến độ, chất lượng code và tuyệt đối không bao giờ xảy ra xung đột mã nguồn (Git Conflict).

---

## 👥 1. PHÂN ROLES & PHẠM VI TRÁCH NHIỆM

Nhằm tối ưu hóa năng suất và độc lập trong quá trình code, 3 thành viên phụ trách các mảng chuyên biệt sau:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      KHANH: DATA / READ ENGINE                                  │
│  - Phụ trách: Database, ORM Models, Migration Alembic                           │
│  - Luồng API: GET /projects (Danh sách), GET /projects/{id} (Chi tiết)          │
│  - Thuật toán: Full-text search 'q', Filter đa điều kiện & Phân trang (W11)     │
│  - Phạm vi file chính: app/models/, app/services/project_service.py (phần GET)  │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────────┐
│     TUYẾT: SCHEMAS & MUTATION/TAGS    │ │       LONG: SECURITY, QA & FRONTEND   │
│ - Phụ trách: Pydantic Schemas & DTOs  │ │ - Phụ trách: Auth JWT, get_current_user│
│ - Luồng API: POST & PUT /projects     │ │ - Luồng API: DELETE /projects/{id}    │
│ - Logic: Auto-upsert `tech_tags`      │ │ - Dữ liệu: Viết script seed_data.py   │
│ - Autocomplete: GET /tech-tags?q=     │ │ - Review & Duyệt merge vào main       │
│ - Phạm vi file: app/schemas/,         │ │ - Kiểm thử: Bộ 5-7 Pytest xương sống  │
│   app/services/tech_tag_service.py    │ │ - Tích hợp: Ghép nối Frontend React   │
└───────────────────────────────────────┘ └───────────────────────────────────────┘
```

### 🔹 1. Khanh (Data / Read Engine)
* **Phụ trách**: Database, ORM Models, Migration Alembic.
* **Luồng API**: `GET /projects` (Danh sách), `GET /projects/{id}` (Chi tiết).
* **Thuật toán**: Full-text search `q`, Filter đa điều kiện & Phân trang (W11).
* **Phạm vi file chính**: `app/models/*`, các hàm đọc trong `app/services/project_service.py`, router GET trong `app/routers/projects.py`.

### 🔹 2. Tuyết (Schemas & Mutation/Tags)
* **Phụ trách**: Pydantic Schemas & DTOs (Request/Response).
* **Luồng API**: `POST /projects`, `PUT /projects/{id}`.
* **Logic**: Tự động Upsert vào `tech_tags` khi tạo hoặc cập nhật dự án (so khớp phân biệt hoa/thường).
* **Autocomplete**: `GET /tech-tags?q=`.
* **Phạm vi file chính**: `app/schemas/*`, `app/services/tech_tag_service.py`, các hàm ghi (create/update) trong `app/services/project_service.py`, router POST/PUT trong `app/routers/projects.py`, router `app/routers/tech_tags.py`.

### 🔹 3. Long (Security, QA & Frontend)
* **Phụ trách**: Auth JWT, dependency `get_current_user`, kiểm tra bảo vệ endpoint.
* **Luồng API**: `DELETE /projects/{id}` (Soft Delete, cập nhật `deleted_at`).
* **Dữ liệu**: Viết script `seed_data.py` (tạo 15-20 records dữ liệu mẫu).
* **Kiểm soát phát hành**: Kiểm tra lần cuối và chịu trách nhiệm merge vào nhánh `main`.
* **Kiểm thử & Ghép nối**: Viết bộ test Pytest tự động và ghép nối trực tiếp với Frontend React.
* **Phạm vi file chính**: `app/core/*`, router `app/routers/auth.py`, hàm soft-delete trong `app/services/project_service.py`, router DELETE trong `app/routers/projects.py`, toàn bộ thư mục `tests/*`.

---

## 📋 2. QUẢN LÝ TASK VÀ TIẾN ĐỘ BACKLOG

1. **Phân công tạo task**: Người đại diện báo cáo của tuần đó sẽ chịu trách nhiệm tạo toàn bộ task WBS của tuần trên Backlog, thiết lập hạn chót (**Start Date**, **Due Date**) và phân công (Assignee) cụ thể cho từng thành viên:
   * **Tuần W10:** Long tạo task & báo cáo tuần.
   * **Tuần W11:** Tuyết tạo task & báo cáo tuần.
   * **Tuần W12:** Khanh tạo task & báo cáo tuần.
2. **Cập nhật trạng thái**: Mỗi thành viên có trách nhiệm chủ động cập nhật trạng thái task theo đúng tiến độ thực tế:
   * **In Progress**: Đang thực hiện.
   * **Resolved**: Đã hoàn thành code, đã test và tạo PR chờ review.
   * **Closed**: Đã merge vào `develop`, test UI thành công và đáp ứng đầy đủ tiêu chuẩn DoD.

---

## 🌿 3. QUY TRÌNH GIT FLOW & QUẢN LÝ MÃ NGUỒN

### 3.1. Quy ước đặt tên nhánh
* **Định dạng**: `feature/w<số_tuần>-<tên_tính_năng>`
* **Ví dụ cụ thể**:
  * `feature/w9-models-and-database` (Khanh)
  * `feature/w9-schemas-and-enums` (Tuyết)
  * `feature/w9-auth-jwt-and-cors` (Long)
  * `feature/w10-create-update-api` (Tuyết)
  * `feature/w10-read-apis` (Khanh)
  * `feature/w10-soft-delete-seed` (Long)

### 3.2. Chiến lược nhánh & Luồng làm việc (Git Flow)
* **`main` (Nhánh chính - Production)**:
  * Chỉ merge khi toàn bộ task trong tuần hoàn thành và test chạy ổn định.
  * **Long phụ trách kiểm tra lần cuối và merge vào nhánh này**.
* **`develop` (Nhánh tích hợp chung - Base branch cho cả team)**:
  * Mọi nhánh tính năng (`feature/...`) đều checkout từ đây và hợp nhất về đây.
  * Quy trình: Tạo Pull Request (PR) $\rightarrow$ Tag thành viên vào review.
  * **Tiêu chuẩn merge**: Có ít nhất **1 Approve** $\rightarrow$ Người tạo PR tự bấm merge vào `develop`.

```text
main (Nhánh chính - Long duyệt & merge cuối tuần)
  │
  └── develop (Nhánh tích hợp chung - Base branch)
        ├── feature/w10-read-apis                     (Khanh)
        ├── feature/w10-create-update-api             (Tuyết)
        └── feature/w10-soft-delete-seed              (Long)
```

### 3.3. Quy ước Commit (Conventional Commits)
Sử dụng tiếng Anh theo chuẩn:
* `feat:` Tính năng mới (VD: `feat: add soft delete logic for projects`)
* `fix:` Sửa lỗi (VD: `fix: return 404 when project is soft deleted`)
* `refactor:` Tối ưu code mà không thay đổi logic nghiệp vụ (VD: `refactor: optimize project filter query`)
* `test:` Thêm hoặc sửa testcase Pytest (VD: `test: add unit test for jwt auth`)
* `docs:` Cập nhật tài liệu

> ⚠️ **Chú ý đặc biệt**: Tuyệt đối **KHÔNG PUSH TRỰC TIẾP** vào nhánh `develop` hoặc `main` khi chưa có Approve.

---

## ✅ 4. TIÊU CHUẨN HOÀN THÀNH TASK (DEFINITION OF DONE - DoD)

Chỉ đóng Task **Closed** trên Backlog khi hoàn thành đầy đủ các điều kiện sau:

- [ ] Code tuân thủ đúng kiến trúc phân tầng, bắt buộc dùng thư mục **`app/services/`** (không dùng `crud/`), không có warning hoặc lỗi linting (format sạch sẽ).
- [ ] Chạy kiểm thử thủ công trên **Swagger UI** hoặc **Postman / REST Client** đạt 100% case (cả trường hợp đúng và các case lỗi 401, 404, 409, 422).
- [ ] Đã viết hoặc cập nhật testcase **Pytest** liên quan.
- [ ] Đã tạo Pull Request, được thành viên còn lại **Approve** và merge vào nhánh `develop` không có xung đột.
- [ ] Đã kiểm tra trực tiếp với **Frontend React** (`npm run dev`), xác nhận dữ liệu hiển thị mượt mà trên UI.
- [ ] Đã cập nhật đầy đủ **Start Date** và **Due Date** trên Backlog.

---

## ⏰ 5. GIAO TIẾP & BÁO CÁO TIẾN ĐỘ HẰNG NGÀY (DAILY SYNC)

Họp nhanh đầu ngày hoặc cập nhật qua nhóm chat chung theo 3 câu hỏi:
1. *Hôm nay đã làm được gì? (Tiến độ % của task hiện tại, phần nào chưa xong?)*
2. *Ngày mai dự kiến làm gì?*
3. *Có gặp khó khăn / blocker nào cần hỗ trợ hoặc thảo luận không?*
