# 01. ĐẶC TẢ 18 TRƯỜNG DỮ LIỆU & QUY TẮC NGHIỆP VỤ PROJECT

---

## 📌 1. Danh sách chi tiết 18 trường của Project

Hệ thống quản lý thông tin dự án yêu cầu đầy đủ 18 trường nghiệp vụ và hệ thống. Dưới đây là bảng chuẩn hóa chi tiết giữa Cơ sở dữ liệu, Pydantic Schema, và Frontend:

| STT | Tên trường (Field Name) | Kiểu dữ liệu Python / DB | Frontend Type | Bắt buộc (Required)? | Ghi chú & Logic nghiệp vụ |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | `id` | `int` (Primary Key) | `number` | **Có (Auto)** | Khóa chính tự tăng trong Database. |
| **2** | `customer_name` | `str` (VARCHAR 255) | `string` | **Có** | Tên khách hàng (bắt buộc nhập, không được để trống hoặc toàn khoảng trắng). |
| **3** | `project_name` | `str` (VARCHAR 255) | `string` | **Có** | Tên dự án (bắt buộc nhập, không được để trống hoặc toàn khoảng trắng). |
| **4** | `description` | `Optional[str]` (TEXT) | `string \| null` | Không | Tóm tắt mô tả dự án. Cho phép `null`. |
| **5** | `industry` | `Optional[str]` (VARCHAR 100) | `string \| null` | Không | Ngành nghề / Lĩnh vực (Ví dụ: E-commerce, Finance, Healthcare...). |
| **6** | `start_date` | `date` (`YYYY-MM-DD`) | `string` | **Có** | Ngày bắt đầu dự án. Bắt buộc nhập định dạng chuẩn ISO ngày. |
| **7** | `end_date` | `Optional[date]` (`YYYY-MM-DD`) | `string \| null` | Không | Ngày kết thúc dự án. **Nếu `is_ongoing = true` thì bắt buộc phải là `null`**. Nếu có, phải `>= start_date`. |
| **8** | `is_ongoing` | `bool` (BOOLEAN, default: `False`) | `boolean` | **Có** | Dự án đang diễn ra (`true`) hay đã kết thúc (`false`). |
| **9** | `team_size` | `Optional[int]` (INTEGER) | `number \| null` | Không | Quy mô đội ngũ (Số lượng nhân sự tham gia, người). Phải là số nguyên `>= 1`. |
| **10** | `total_man_month` | `Optional[float]` (NUMERIC / FLOAT) | `number \| null` | Không | Tổng quy mô nhân tháng (**man-month, TUYỆT ĐỐI KHÔNG PHẢI TIỀN TỆ**). Phải là số thực dương `>= 0.0`. |
| **11** | `team_composition_note` | `Optional[str]` (TEXT) | `string \| null` | Không | Ghi chú chi tiết về cơ cấu đội ngũ (VD: 1 PM, 2 BrSE, 5 Dev, 2 Tester...). |
| **12** | `technologies` | `List[str]` (CSV hoặc JSON trong DB) | `string[]` | Không | Danh sách tag công nghệ (VD: `["FastAPI", "React", "Docker"]`). |
| **13** | `project_types` | `List[str]` (CSV hoặc JSON trong DB) | `ProjectTypeCode[]` | Không | Danh sách mã phân loại dự án (Lấy từ bộ Enum chuẩn). |
| **14** | `dev_process_phases` | `List[str]` (CSV hoặc JSON trong DB) | `DevProcessPhaseCode[]` | Không | Danh sách các công đoạn phát triển tham gia (Lấy từ bộ Enum chuẩn). |
| **15** | `outcome_note` | `Optional[str]` (TEXT) | `string \| null` | Không | Kết quả, bài toán thực tế và giải pháp (成果・課題・解決策). |
| **16** | `source_note` | `Optional[str]` (TEXT) | `string \| null` | Không | Ghi chú nguồn gốc thông tin / tài liệu tham khảo (確認元メモ). |
| **17** | `created_by` | `str` (VARCHAR 255) | `string` | **Có (Auto)** | Email của người tạo bản ghi. Lấy trực tiếp từ JWT Bearer Token của user đang đăng nhập. |
| **18** | `created_at` | `datetime` (TIMESTAMP UTC) | `string` (ISO) | **Có (Auto)** | Thời gian tạo bản ghi hệ thống. |
| * | `updated_at` | `datetime` (TIMESTAMP UTC) | `string` (ISO) | **Có (Auto)** | Thời gian cập nhật gần nhất. |
| * | `deleted_at` | `Optional[datetime]` (TIMESTAMP) | `—` | Không | Cột cờ phục vụ **Soft Delete** (`null` = hoạt động, khác `null` = đã xóa). |

---

## 🏷️ 2. Giá trị chuẩn của 2 bộ Enums

Frontend đã cố định các mã code và nhãn hiển thị tiếng Nhật tương ứng. Backend phải validate chặt chẽ, chỉ cho phép các giá trị thuộc danh sách dưới đây:

### 2.1. Enum `project_types` (Loại hình dự án)
Định nghĩa tại [`InternTraining-Project-Tracking/src/lib/projectTypes.ts`](../InternTraining-Project-Tracking/src/lib/projectTypes.ts):

| Mã Code (Lưu DB & API) | Nhãn Tiếng Nhật (Hiển thị UI) | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| `"offshore"` | オフショア | Dự án phát triển dạng Offshore |
| `"ses"` | SES | Hợp đồng nhân sự IT (System Engineering Service) |
| `"lab"` | ラボ | Dự án ODC (Labo / Dedicated Team) |
| `"new_dev"` | 新規開発 | Phát triển dự án mới từ đầu (Greenfield) |
| `"maintenance"` | 保守 | Dự án bảo trì, vận hành nâng cấp (Maintenance) |

### 2.2. Enum `dev_process_phases` (Công đoạn phát triển)
Định nghĩa tại [`InternTraining-Project-Tracking/src/lib/devProcessPhases.ts`](../InternTraining-Project-Tracking/src/lib/devProcessPhases.ts):

| Mã Code (Lưu DB & API) | Nhãn Tiếng Nhật (Hiển thị UI) | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| `"requirements"` | 要件定義 | Định nghĩa yêu cầu khách hàng |
| `"design"` | 設計 | Thiết kế hệ thống (Basic / Detail Design) |
| `"implementation"` | 実装 | Lập trình / Coding |
| `"testing"` | テスト | Kiểm thử (Unit, Integration, System Test) |
| `"release"` | リリース | Đóng gói và phát hành sản phẩm |
| `"maintenance_ops"`| 保守運用 | Vận hành và giám sát sau triển khai |

---

## ⚙️ 3. Các quy tắc nghiệp vụ đặc biệt (Business Rules)

### 3.1. Cơ chế tự động Upsert vào `tech_tags`
* **Khi nào kích hoạt?**: Khi gọi API `POST /projects` (Tạo mới) hoặc `PUT /projects/{id}` (Cập nhật).
* **Quy trình xử lý (Đã chốt với Mentor - Q4)**:
  1. Người dùng gửi lên mảng công nghệ: ví dụ `technologies: ["React", "FastAPI", "Docker"]`.
  2. Hệ thống duyệt qua từng tag (chuẩn hóa `trim` khoảng trắng):
     * Tìm trong bảng `tech_tags` theo **so khớp phân biệt hoa thường (case-sensitive)** (`TechTag.name == tag_name`).
     * Ví dụ: Nếu đã có tag `"react"` mà client gửi `"React"`, hệ thống **vẫn tạo mới bản ghi `"React"`** trong `tech_tags`.
     * Nếu đã tồn tại chính xác tên tag: Tái sử dụng tag có sẵn.
  3. **Lưu ý khi xóa dự án**: Khi xóa dự án (Soft Delete), **vẫn giữ nguyên toàn bộ các tag trong bảng `tech_tags`**, không xóa tag đi.
* **API Autocomplete `GET /tech-tags?q=...`**:
  * Tìm kiếm theo từ khóa `q` trong bảng `tech_tags`.
  * Không phân biệt hoa thường (`ILIKE %q%`).
  * Nếu `q` rỗng: Trả về danh sách tag (giới hạn tối đa 20 bản ghi).
  * Nếu có `q`: Tìm gần đúng, trả về tối đa 20 kết quả dạng mảng string `["React", "React Native"]`.

### 3.2. Cơ chế Soft Delete (`DELETE /projects/{id}`)
* **Tuyệt đối không xóa vật lý**: Không thực hiện lệnh `DELETE FROM projects WHERE id = ...`.
* **Cập nhật mốc thời gian**: Gán `deleted_at = datetime.utcnow()` và lưu lại DB.
* **Tác động đến các API khác (Đã chốt với Mentor - Q1)**:
  * `GET /projects` (Danh sách): Tự động thêm điều kiện truy vấn `WHERE deleted_at IS NULL`. Các dự án đã xóa mặc định ẩn khỏi danh sách.
  * `GET /projects/{id}` (Chi tiết): Nếu `id` không có trong DB hoặc đã có `deleted_at IS NOT NULL` $\rightarrow$ Trả về mã lỗi `404 Not Found`.
  * `PUT /projects/{id}` (Cập nhật): Nếu dự án đã bị soft delete $\rightarrow$ Trả về mã lỗi `404 Not Found`.
  * `DELETE /projects/{id}` (Xóa lại): Nếu đã bị xóa trước đó $\rightarrow$ Trả về `404 Not Found`.

### 3.3. Ràng buộc ngày tháng & tiến độ (`is_ongoing` vs `end_date`) (Đã chốt với Mentor - Q2)
* **Bắt buộc**: `end_date >= start_date` (nếu có nhập `end_date`).
* **Logic xung đột**: Nếu `is_ongoing = true` mà client gửi kèm cả `end_date`, Backend **bắt buộc trả lỗi HTTP `422 Unprocessable Entity`** (thông báo: *"進行中の場合、終了日は入力できません"*), không tự động ép về null để đảm bảo tính tường minh.

### 3.4. Chấp nhận mảng rỗng `[]` ở phân loại & công đoạn (Đã chốt với Mentor - Q3)
* Client gửi `project_types: []` hoặc `dev_process_phases: []` thì **vẫn hoàn toàn hợp lệ và cho phép tạo dự án**.
* Trong DB lưu dưới dạng chuỗi rỗng `""`. Khi đọc ra API, trả về mảng rỗng `[]`.

### 3.5. Chuẩn hóa dữ liệu quy mô (`total_man_month` & `team_size`)
* **`total_man_month`**: Đơn vị là **nhân-tháng (man-month)**, đại diện cho khối lượng công việc (1 người làm trong 1 tháng). **Đây KHÔNG PHẢI là số tiền kinh phí hay ngân sách (Cost/Budget)**. Validate kiểu số thực dương (`float >= 0`).
* **`team_size`**: Số lượng thành viên tham gia đồng thời. Validate số nguyên dương (`int >= 1`).

### 3.6. Giới hạn phân trang `page_size` (Đã chốt với Mentor - Q6)
* Tham số `page_size`: Mặc định là `20`, **giới hạn tối đa `max = 1000`** (`Query(20, ge=1, le=1000)`).

### 3.7. Cơ chế Auth, Token & Quyền Sửa/Xóa (Đã chốt với Mentor - Q7, Q8, Q9)
* **Thời hạn Token**: Token JWT có thời hạn sống là **24 giờ** (`ACCESS_TOKEN_EXPIRE_MINUTES = 1440`). Không cần cơ chế Refresh Token; khi hết hạn Frontend redirect về `/login`.
* **Phân quyền**: Tạm thời **chưa cần phân quyền riêng cho Admin**, chỉ cần user đăng nhập hợp lệ.
* **Quyền Sửa/Xóa**: **Bất kỳ ai đăng nhập trong hệ thống cũng đều có quyền sửa/xóa dự án của nhau**, không ràng buộc chỉ người tạo (`created_by`) mới được sửa/xóa.
* **Gán người tạo**: Tự động lấy `email` từ JWT Token gán vào `created_by` khi gọi `POST /projects`.
