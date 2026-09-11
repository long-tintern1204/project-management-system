# 04. LỘ TRÌNH 4 TUẦN (W09 – W12) & KẾ HOẠCH HẰNG NGÀY (DAY-BY-DAY)

---

## 📅 1. Bức tranh tổng thể 4 tuần (W09 – W12)

Dựa trên bảng kế hoạch đào tạo chính thức của Mentor:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ W09: Kickoff hệ thống quản lý 実績 + Chốt Scope/Backlog    (Long báo cáo tuần)  │
│ - Đọc kỹ tài liệu API仕様, Q&A với mentor để chốt 18 fields, enums, soft delete │
│ - Tạo model 'projects' (technologies_csv, project_types_csv, deleted_at)        │
│ - Tạo bảng 'tech_tags' + chạy migration Alembic                                 │
│ - Tích hợp Auth /auth/register + /auth/login, bảo vệ endpoint bằng JWT          │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W10: Implement Project APIs (Backend) CRUD theo đúng Spec (Khanh báo cáo)       │
│ - CRUD Project: POST /projects, GET /projects (cơ bản), GET /{id}, PUT, DELETE  │
│ - Validate 18 fields + enums project_types/dev_process_phases                   │
│ - technologies: Tự động upsert vào tech_tags khi tạo/cập nhật                   │
│ - DELETE: Soft delete (gán deleted_at, không xóa vật lý)                        │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W11: Filter / Search + Pagination + Tech-tags Autocomplete (Tuyết báo cáo tuần) │
│ - Filter multi-value (OR trong từng field, AND giữa các field khác nhau)        │
│ - Full-text search 'q' trên customer_name, project_name, description            │
│ - Pagination chuẩn: page, page_size, total                                      │
│ - GET /tech-tags?q= autocomplete (case-insensitive, max 20, q rỗng trả all)     │
│ - Chuẩn hoá total_man_month (man-month, KHÔNG PHẢI TIỀN) và team_size           │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────────────┐
│ W12: Tests tối thiểu + Final Docs + Final Demo (Cả 3 báo cáo tuần & demo)     │
│ - 5–7 Pytest tests "xương sống" (Auth, CRUD, Soft delete, Filter, Tech-tags)   │
│ - README backend hoàn chỉnh + Kịch bản Demo 6–8 bước                           │
│ - Fix bug, nghiệm thu, retro và nộp báo cáo cá nhân                            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗓️ 2. Kế hoạch hằng ngày chi tiết cho TUẦN 2 (W10: Implement CRUD Project APIs)
**Người đại diện báo cáo tuần W10:** **Long**

| Ngày | Mục tiêu chính | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Long (Security, QA & Frontend) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Khởi động tuần & Setup Schemas** | - Review lại cấu trúc DB `projects` và `tech_tags`.<br>- Dựng khung hàm `get_by_id()`, `list_projects()`. | - Viết Pydantic schemas: `ProjectCreateInput`, `ProjectResponse`.<br>- Viết validator 18 fields & 2 enums. | - Kiểm tra module Auth JWT hoạt động ổn định.<br>- Viết dependency `get_current_user`. | Swagger `/docs` hiển thị đủ Schemas; Auth trả về token thành công. |
| **Thứ 3 (Day 2)** | **Auto-upsert Tag & Soft Delete** | - Viết logic `get_by_id()` lọc `deleted_at IS NULL` (báo 404 nếu đã xóa).<br>- Viết query `list_projects()` cơ bản. | - Viết `tech_tag_service.py` với logic `upsert_tags()`.<br>- Bắt đầu viết `create()` project. | - Viết logic `soft_delete()` gán `deleted_at = datetime.utcnow()`.<br>- Bắt đầu viết file `seed_data.py`. | Chạy thử upsert tag: tag mới được thêm, tag cũ không bị trùng lặp. |
| **Thứ 4 (Day 3)** | **Hoàn thiện API POST / PUT / DELETE** | - Viết router `GET /projects/{id}`.<br>- Viết router `GET /projects` (danh sách cơ bản, lọc soft-delete). | - Hoàn thiện API `POST /projects` (lấy email từ JWT gán `created_by`).<br>- Hoàn thiện API `PUT /projects/{id}`. | - Hoàn thiện API `DELETE /projects/{id}` (trả về 204 hoặc 200).<br>- Tạo 15-20 records mẫu qua file seed. | Chạy toàn bộ 5 API CRUD trên Swagger UI: Tạo $\rightarrow$ Xem chi tiết $\rightarrow$ Cập nhật $\rightarrow$ Xóa. |
| **Thứ 5 (Day 4)** | **Code Review chéo & Sửa lỗi** | - Kiểm tra dữ liệu mảng CSV khi đọc ra có đúng kiểu `List[str]`.<br>- Review PR của Tuyết. | - Kiểm tra validation edge cases (nhập `end_date` khi `is_ongoing=true`).<br>- Review PR của Long. | - Viết 3 testcase Pytest cơ bản: Tạo project, Sửa project, Xóa soft delete.<br>- Review PR của Khanh. | 3 PRs được merge vào nhánh `develop`; Testcase pass xanh 100%. |
| **Thứ 6 (Day 5)** | **Ghép nối Frontend React & Báo cáo tuần** | - Cùng Tuyết và Long bật Frontend React (`npm run dev`), kiểm tra hiển thị Card/List. | - Kiểm tra Form Create & Edit trên giao diện React có gửi đúng 18 fields không. | - Kiểm tra nút Xóa trên UI mở Modal và gọi đúng API DELETE.<br>- **Long kiểm tra lần cuối và merge `develop` vào `main`**. | Frontend React thao tác mượt mà với Backend; **Long đại diện báo cáo tuần W10**. |

---

## 🗓️ 3. Kế hoạch hằng ngày chi tiết cho TUẦN 3 (W11: Filter, Search & Pagination)
**Người đại diện báo cáo tuần W11:** **Tuyết**

| Ngày | Mục tiêu chính | Khanh (Data / Read Engine) | Tuyết (Schemas & Mutation/Tags) | Long (Security, QA & Frontend) | Tiêu chí hoàn thành (DoD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Phân tích thuật toán lọc** | - Thiết kế Query Builder: Xử lý logic lọc (OR trong từng field, AND giữa các field). | - Viết API `GET /tech-tags?q=` (không phân biệt hoa thường, giới hạn 20 kết quả). | - Rà soát lại tất cả endpoint để đảm bảo bắt buộc có header JWT. | Thống nhất cấu trúc query params cho `GET /projects`. |
| **Thứ 3 (Day 2)** | **Full-text search & Pagination** | - Triển khai tìm kiếm `q` trên 3 cột: `customer_name`, `project_name`, `description`.<br>- Viết phân trang chuẩn (`page`, `page_size`, `total`). | - Tối ưu hóa `search_tags`: Nếu `q` rỗng thì trả về top 20 tag mới nhất.<br>- Chuẩn hóa trường `total_man_month` (man-month). | - Cập nhật dữ liệu `seed_data.py` thêm nhiều tag phong phú để test tìm kiếm.<br>- Viết testcase cho Autocomplete tag. | API `GET /projects?page=1&page_size=20&q=...` trả về đúng định dạng JSON. |
| **Thứ 4 (Day 3)** | **Tích hợp bộ lọc phức tạp** | - Hoàn thiện lọc đồng thời: `technology` + `project_type` + `dev_process_phase`.<br>- Tối ưu hóa câu truy vấn SQL để không bị chậm. | - Chuẩn hóa validate `team_size` (số nguyên) và `total_man_month` (số thực).<br>- Viết tài liệu hướng dẫn tham số query. | - Viết testcase kiểm thử kết hợp nhiều bộ lọc cùng lúc.<br>- Kiểm tra phân trang khi dữ liệu bị lọc. | Lọc nhiều tag cùng lúc: Dự án có tag A HOẶC tag B đều hiện; Kết hợp khác loại thì AND. |
| **Thứ 5 (Day 4)** | **Code Review & Tối ưu hiệu năng** | - Review code, đánh Index cho các cột tìm kiếm để tăng tốc DB.<br>- Merge PR vào `develop`. | - Kiểm tra tính tương thích với Frontend Autocomplete Component.<br>- Merge PR vào `develop`. | - Chạy toàn bộ Pytest kiểm thử bộ lọc.<br>- Merge PR vào `develop`. | Toàn bộ tính năng W11 hợp nhất trên nhánh `develop`; Tuyết chuẩn bị báo cáo. |
| **Thứ 6 (Day 5)** | **Ghép nối toàn diện với Frontend** | - Test trực tiếp thanh tìm kiếm và bộ lọc dropdown trên giao diện React.<br>- Test nút phân trang (Next/Prev). | - Test gõ chữ vào ô nhập công nghệ trên UI xem có hiển thị gợi ý tag xổ xuống không. | - Kiểm tra các filter chip màu trên giao diện (xóa từng chip, nút xóa tất cả).<br>- **Long merge `develop` vào `main`**. | Giao diện danh sách dự án lọc mượt mà, phản hồi tìm kiếm tức thì; **Tuyết đại diện báo cáo tuần W11**. |

---

## 🗓️ 4. Kế hoạch hằng ngày chi tiết cho TUẦN 4 (W12: Tests, Docs & Final Demo)
**Người đại diện báo cáo tuần W12:** **Khanh**

| Ngày | Mục tiêu chính | Nhiệm vụ của cả Team 3 người (Long, Khanh, Tuyết) |
| :--- | :--- | :--- |
| **Thứ 2 (Day 1)** | **Viết bộ kiểm thử xương sống (5–7 Pytest)** | - **Long chủ trì**: Viết các testcase cốt lõi (Auth 409/401, CRUD 18 fields, Soft delete 404, Filter search, Tech tags).<br>- **Khanh & Tuyết**: Hỗ trợ viết mock data và fixture DB trong `tests/conftest.py`. |
| **Thứ 3 (Day 2)** | **Sửa lỗi tồn đọng (Bug Fixing)** | - Cả 3 người rà soát danh sách bug phát hiện từ test và giao diện.<br>- Sửa triệt để các lỗi lệch kiểu dữ liệu, lỗi múi giờ UTC, lỗi validation message tiếng Nhật. |
| **Thứ 4 (Day 3)** | **Hoàn thiện tài liệu bàn giao (Final Docs)** | - Viết file `README.md` chính ở root: Hướng dẫn cài đặt, thiết lập môi trường `.env`, chạy migration, tài khoản test mẫu, lệnh chạy app & test.<br>- Đảm bảo người khác clone repo về có thể chạy ngay mà không gặp lỗi. |
| **Thứ 5 (Day 4)** | **Tổng duyệt kịch bản Demo 6–8 bước** | Cả 3 thành viên cùng luyện tập kịch bản demo mẫu trước mentor:<br>1. Đăng ký tài khoản mới $\rightarrow$ Báo 409 nếu trùng email.<br>2. Đăng nhập $\rightarrow$ Nhận JWT token.<br>3. Tạo dự án mới với đầy đủ 18 trường + nhập tag công nghệ mới.<br>4. Mở danh sách: Kiểm tra tag vừa tạo xuất hiện trong bộ lọc $\rightarrow$ Thử autocomplete.<br>5. Tìm kiếm từ khóa `q` + Lọc theo `project_type` & `technology`.<br>6. Mở xem chi tiết dự án $\rightarrow$ Chỉnh sửa thông tin.<br>7. Bấm xóa dự án (Soft delete) $\rightarrow$ Xác nhận không còn ở danh sách & xem chi tiết báo 404.<br>8. Kiểm tra cơ sở dữ liệu xác nhận bản ghi vẫn còn nhưng có `deleted_at`. |
| **Thứ 6 (Day 5)** | **Final Demo, Retro & Nghiệm thu** | - **Khanh dẫn dắt buổi Demo chính thức với Mentor**, Long và Tuyết hỗ trợ giải đáp kỹ thuật.<br>- Tiến hành buổi Retrospective (Họp rút kinh nghiệm nhóm).<br>- Nộp báo cáo cá nhân hoàn thành khóa đào tạo thực tập. |
