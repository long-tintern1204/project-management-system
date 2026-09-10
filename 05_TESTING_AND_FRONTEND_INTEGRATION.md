# 05. CHECKLIST KIỂM THỬ & LƯU Ý TÍCH HỢP FRONTEND REACT

---

## 🧪 1. Bộ kiểm thử Pytest "xương sống" (Core Test Suite)

Theo yêu cầu chuẩn đầu ra của tuần **W12**, Backend bắt buộc phải có từ **5 đến 7 testcase cốt lõi** bao phủ toàn bộ các luồng nghiệp vụ quan trọng nhất. Dưới đây là danh sách testcase chi tiết để Team triển khai:

| STT | Tên Test Case | Mục đích kiểm thử | Kết quả mong đợi |
| :---: | :--- | :--- | :--- |
| **Test 1** | `test_auth_conflict_and_invalid_login` | Kiểm tra xử lý ngoại lệ Auth | - Đăng ký email đã tồn tại $\rightarrow$ Trả về mã **`409 Conflict`**.<br>- Đăng nhập sai mật khẩu $\rightarrow$ Trả về mã **`401 Unauthorized`**. |
| **Test 2** | `test_unauthorized_access` | Kiểm tra bảo vệ endpoint bằng JWT | Gọi `GET /projects` hoặc `POST /projects` mà không kèm header `Authorization: Bearer <token>` $\rightarrow$ Trả về **`401 Unauthorized`**. |
| **Test 3** | `test_create_project_and_validation` | Kiểm tra tạo mới và validate 18 trường | - Tạo thành công khi đủ trường bắt buộc $\rightarrow$ Trả về **`201 Created`**.<br>- Thiếu `customer_name` hoặc `project_name` $\rightarrow$ Trả về **`422 Unprocessable Entity`**.<br>- Nhập `is_ongoing=True` kèm `end_date` $\rightarrow$ Trả về **`422`**. |
| **Test 4** | `test_tech_tags_auto_upsert` | Kiểm tra tự động upsert tag công nghệ (Q4 Mentor) | - Gọi `POST /projects` với `technologies: ["VueJS", "Docker"]`. Bảng `tech_tags` tự động có `"VueJS"` và `"Docker"`.<br>- Tạo tiếp với `["vuejs"]` $\rightarrow$ Bảng có thêm `"vuejs"` (so khớp phân biệt hoa thường).<br>- Sau khi `DELETE /projects/{id}`, các tag trong `tech_tags` vẫn được giữ nguyên không bị xóa. |
| **Test 5** | `test_soft_delete_and_not_found` | Kiểm tra tính năng xóa mềm (Soft Delete) | - Gọi `DELETE /projects/{id}` $\rightarrow$ Trả về **`204`** hoặc **`200`**.<br>- Gọi `GET /projects/{id}` với ID vừa xóa $\rightarrow$ Trả về **`404 Not Found`**.<br>- Gọi `GET /projects` $\rightarrow$ Project vừa xóa **không còn xuất hiện** trong danh sách. |
| **Test 6** | `test_filter_and_search_pagination` | Kiểm tra tìm kiếm `q`, bộ lọc và phân trang (Q5, Q6 Mentor) | - Tìm kiếm `q="Alpha"` $\rightarrow$ Chỉ trả về dự án có chứa `"Alpha"` trong tên/khách hàng/mô tả.<br>- Lọc đồng thời theo `technology` (OR) và `project_type` (OR), kết hợp 2 trường là AND.<br>- Kiểm tra cấu trúc: `items`, `total`, `page`, `page_size`. Chặn `page_size > 1000` ném lỗi `422`. |
| **Test 7** | `test_tech_tags_autocomplete` | Kiểm tra gợi ý tìm kiếm tag | - Gọi `GET /tech-tags?q=py` $\rightarrow$ Trả về danh sách chứa `"Python"`, không phân biệt hoa thường, giới hạn tối đa 20 kết quả.<br>- Gọi `GET /tech-tags` (không có `q`) $\rightarrow$ Trả về toàn bộ tag (tối đa 20). |

---

## 🔗 2. Checklist kiểm tra tích hợp thực tế với Frontend React

Frontend đã được xây dựng sẵn trong thư mục [`InternTraining-Project-Tracking/`](../InternTraining-Project-Tracking). Để hai bên chạy mượt mà ngay lần đầu kết nối, team cần kiểm tra từng mục sau:

### ✅ 2.1. Cấu hình Cổng kết nối & Môi trường
- [ ] Backend FastAPI chạy tại: `http://localhost:8000` (hoặc `http://127.0.0.1:8000`).
- [ ] Frontend React chạy tại: `http://localhost:5173`.
- [ ] Kiểm tra file `.env` của Frontend đã có biến:
  ```env
  VITE_API_BASE_URL=http://localhost:8000
  ```

### ✅ 2.2. Kiểm tra CORS (Cross-Origin Resource Sharing)
- [ ] Backend FastAPI đã kích hoạt `CORSMiddleware`.
- [ ] Cấu hình cho phép nguồn `http://localhost:5173`:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- [ ] Nếu CORS chưa cấu hình đúng, trình duyệt sẽ chặn request và báo lỗi: *`Access to fetch at ... from origin ... has been blocked by CORS policy`*.

### ✅ 2.3. Kiểm tra định dạng Token và Tiêu đề Xác thực (Authorization Header)
- [ ] Frontend gửi token qua header: `Authorization: Bearer <token>`.
- [ ] Token JWT chứa payload có trường `email` (dạng string) và `role` (`admin` hoặc `member`) để giao diện hiển thị thông tin người dùng đăng nhập.
- [ ] Khi token hết hạn hoặc không hợp lệ, Backend phải trả về đúng mã **`401`** (Frontend đã có sẵn cơ chế tự động xóa token và chuyển hướng về trang `/login` khi nhận `401`).

### ✅ 2.4. Kiểm tra định dạng danh sách trả về (Pagination Response)
- [ ] Endpoint `GET /projects` bắt buộc phải trả về JSON Object có cấu trúc chính xác:
  ```json
  {
    "items": [ /* Danh sách các project */ ],
    "total": 105,
    "page": 1,
    "page_size": 20
  }
  ```
  *(Nếu Backend chỉ trả về mảng `[...]` thay vì object có `items` và `total`, trang `ProjectList.tsx` của Frontend sẽ bị trắng màn hình do lỗi `undefined items`)*.

---

## ⚠️ 3. Các lỗi phổ biến (Common Pitfalls) và Cách khắc phục

### 🚩 Bẫy 1: Chuỗi rỗng `""` so với `null`
* **Vấn đề**: Khi người dùng không nhập các trường tùy chọn trên Form (như `description`, `industry`, `outcome_note`), Frontend có thể gửi lên chuỗi rỗng `""`.
* **Khắc phục**: Trong Pydantic schema hoặc Service, chuyển toàn bộ chuỗi rỗng `""` hoặc chuỗi toàn khoảng trắng thành `None`/`null` trước khi lưu vào DB. Khi trả về API, các trường không có dữ liệu phải hiển thị là `null` để Frontend hiển thị ký tự gạch nối `" — "` chuẩn nghiệp vụ.

### 🚩 Bẫy 2: Chuyển đổi giữa mảng `List[str]` và chuỗi `CSV` trong Database
* **Vấn đề**: Khi lưu trong DB bảng đơn `projects`, ta lưu dạng chuỗi: `technologies_csv = "FastAPI,React,Docker"`.
* **Khắc phục**:
  * Khi lưu vào DB: Dùng `",".join(input.technologies)`.
  * Khi đọc từ DB ra API: Tách chuỗi bằng `.split(",")` và loại bỏ chuỗi rỗng:
    ```python
    technologies = [t.strip() for t in project.technologies_csv.split(",") if t.strip()]
    ```
  * Luôn đảm bảo API trả về cho Frontend là mảng `["FastAPI", "React", "Docker"]`, tuyệt đối không trả về chuỗi `"FastAPI,React,Docker"`.

### 🚩 Bẫy 3: Sai lệch định dạng ngày tháng (Date format)
* **Vấn đề**: Trường `start_date` và `end_date` bị lẫn lộn giữa định dạng `YYYY-MM-DD` và định dạng đầy đủ có cả giờ `YYYY-MM-DDTHH:MM:SSZ`.
* **Khắc phục**: Dùng kiểu `date` (không có time) trong Pydantic và SQLAlchemy cho hai trường này. Khi trả về JSON, đảm bảo chỉ có định dạng ngày chuẩn `YYYY-MM-DD` (VD: `"2026-04-01"`).

### 🚩 Bẫy 4: Nhầm lẫn bản chất của `total_man_month`
* **Vấn đề**: Hiểu nhầm `total_man_month` là số tiền lương hoặc kinh phí dự án, dẫn đến nhập dữ liệu hàng trăm triệu hoặc định dạng sai.
* **Khắc phục**: Đây là **nhân-tháng (man-month)**, thể hiện tổng khối lượng nhân công (ví dụ dự án 5 người làm trong 3 tháng có quy mô khoảng 15 man-month). Validate kiểu số thực (`float`), không gắn ký hiệu tiền tệ (`$`, `VNĐ`, `¥`).
