# BẢNG Q&A XÁC NHẬN SPEC VỚI MENTOR (KẾT QUẢ CHÍNH THỨC)

**Dự án:** プロジェクト管理システム (Project Performance Management System)  
**Team:** Tuyết, Long, Khanh  
**Thời gian xác nhận:** Tuần W09 (Kickoff)  
**Trạng thái:** ✅ Đã hoàn thành xác nhận và có câu trả lời chính thức từ Mentor.

---

## 📊 BẢNG TỔNG HỢP CÂU HỎI & CÂU TRẢ LỜI CỦA MENTOR

| STT | Vấn đề cần làm rõ | Câu trả lời chính thức của Mentor | Hướng xử lý kỹ thuật của Team |
| :---: | :--- | :--- | :--- |
| **Q1** | Lọc bản ghi xóa mềm ở API danh sách dự án (`GET /projects`) | **Đúng** | Tự động thêm điều kiện `WHERE deleted_at IS NULL` trong query danh sách để mặc định ẩn các dự án đã xóa. |
| **Q2** | Ràng buộc ngày tháng (`end_date >= start_date`) và logic `is_ongoing` | **Backend sẽ validate bắt buộc `end_date >= start_date`. Và khi dự án đang diễn ra (`is_ongoing = true`), nếu client gửi kèm cả `end_date` thì Backend nên trả lỗi** | Dùng `@model_validator` trong Pydantic. Nếu `is_ongoing=True` mà `end_date is not None` $\rightarrow$ ném lỗi HTTP `422` (*"進行中の場合、終了日は入力できません"*). Kiểm tra `end_date >= start_date`. |
| **Q3** | Validate mảng rỗng `[]` ở `project_types` và `dev_process_phases` | **Client gửi mảng rỗng thì vẫn hợp lệ và cho phép tạo dự án** | Field `project_types` và `dev_process_phases` cho phép nhận `[]` (Default: `[]`), lưu vào DB dưới dạng chuỗi rỗng `""`. |
| **Q4** | Xử lý trùng chữ hoa / thường khi tự động Upsert `tech_tags` | **Khi upsert tag, Backend sẽ so khớp phân biệt hoa thường (ví dụ nếu đã tồn tại 'react' mà có thêm 'React' thì vẫn tạo mới). Khi xóa project thì vẫn giữ nguyên các tag trong `tech_tags`** | Trong hàm `upsert_tags`: So sánh chính xác theo chữ hoa/thường (`TechTag.name == tag_name`). Không xóa tag trong `tech_tags` khi project bị soft delete. |
| **Q5** | Logic kết hợp giữa các bộ lọc (Multi-value Filter: AND hay OR?) | **Đúng** | Trong cùng một field (nhiều tag hoặc nhiều type): điều kiện **OR**. Giữa các field khác nhau (ví dụ: vừa lọc technology vừa lọc project_type): điều kiện **AND**. |
| **Q6** | Giới hạn cận trên của tham số phân trang `page_size` | **Set giới hạn max = 1000** | Trong query parameter: `page_size: int = Query(20, ge=1, le=1000)`. Mặc định là 20, tối đa 1000. |
| **Q7** | Vai trò `role` trong bảng `users` và phạm vi tài khoản Admin | **Tạm thời chưa cần tính năng phân quyền** | Vẫn lưu cột `role` trong bảng `users` (default: `'member'`), nhưng chưa cần viết logic chặn quyền Admin/Member ở các API. Chỉ cần xác thực JWT thành công. |
| **Q8** | Thời hạn sống của JWT Token & Refresh Token | **Thời gian sống của token để 24h. Khi token hết hạn thì phía Frontend chỉ cần redirect về trang `/login` để đăng nhập lại, không cần cơ chế Refresh Token** | Cấu hình `ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24` (24 tiếng). Khi token hết hạn, API trả về `401 Unauthorized`. Frontend tự động logout và chuyển hướng về `/login`. |
| **Q9** | Quyền Sửa/Xóa dự án: Có ràng buộc theo người tạo (`created_by`) không? | **Bất kỳ ai đăng nhập trong hệ thống cũng đều có quyền sửa/xóa dự án của nhau** | API `PUT /projects/{id}` và `DELETE /projects/{id}` chỉ cần yêu cầu đăng nhập hợp lệ (có Bearer JWT), không kiểm tra xem `current_user.email == project.created_by`. |
| **Q10**| Chuẩn bị dữ liệu mẫu (Seed Data) cho buổi Demo W12 | **OK. Team tự tạo dữ liệu mẫu** | Long viết script `seed_data.py` nạp sẵn 15–20 dự án mẫu có đầy đủ tags, dates, phases đa dạng để test mượt mà các luồng filter và paging trong buổi demo W12. |

---

## 🔍 CHI TIẾT NỘI DUNG Q&A VỚI MENTOR

### 1. VỀ NGHIỆP VỤ & VALIDATE DỮ LIỆU

#### Q1. Lọc bản ghi xóa mềm ở API danh sách dự án
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 5 (`DELETE /projects/{id}`, dòng 80-85): Cột Description ghi `deleted_atに現在時刻をセット（論理削除）`.
  * Sheet `API詳細` - Mục 3 (`GET /projects/{id}`, dòng 68): Phần Constraint ghi `存在しない or 削除済み → 404 Not Found`.
  * Sheet `API詳細` - Mục 1 (`GET /projects`, dòng 4-11): Bảng Request hoàn toàn không có tham số hay ghi chú điều kiện lọc về `deleted_at`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 5 DELETE spec yêu cầu lưu vết bằng deleted_at, và ở Mục 3 (GET id) có ghi rõ là nếu đã xóa thì báo 404. Nhưng ở Mục 1 (GET danh sách) thì không thấy ghi điều kiện lọc hay tham số gì về deleted_at. Em muốn confirm lại là: Backend sẽ tự động thêm điều kiện WHERE deleted_at IS NULL khi lấy danh sách để mặc định ẩn các dự án đã xóa, đúng không ạ?"*
* **Mentor trả lời:** **Đúng**.

---

#### Q2. Ràng buộc ngày tháng (`end_date >= start_date`) và logic `is_ongoing`
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 2 (`POST /projects`, dòng 25-27): `start_date` (Required: Yes, YYYY-MM-DD), `end_date` (Required: No, YYYY-MM-DD), `is_ongoing` (Required: No, default=false).
  * Sheet `データモデル` (dòng 16-18): Cột Constraints không có ràng buộc liên trường giữa `is_ongoing` và `end_date`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 2 (POST) và sheet データモデル, spec chỉ ghi định dạng ngày YYYY-MM-DD và chưa có ràng buộc chéo. Nếu có nhập end_date thì Backend sẽ validate bắt buộc end_date >= start_date, đúng không ạ? Và khi dự án đang diễn ra (is_ongoing = true), nếu client gửi kèm cả end_date thì Backend nên tự động ép về null hay ném lỗi 422 để bắt sửa lại ạ? (Team em đề xuất ném lỗi 422: '進行中の場合、終了日は入力できません')."*
* **Mentor trả lời:**  
  **"Backend sẽ validate bắt buộc end_date >= start_date. Và khi dự án đang diễn ra (is_ongoing = true), nếu client gửi kèm cả end_date thì Backend nên trả lỗi"**.

---

#### Q3. Validate mảng rỗng `[]` ở `project_types` và `dev_process_phases`
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 2 (`POST /projects`, dòng 35,36): 2 trường `project_types` và `dev_process_phases` đều ghi Required: No.
  * Sheet `API詳細` - Mục 1 (`GET /projects`, dòng 10-11): Cột Default ghi rõ là `[]`.
  * Sheet `データモデル` (dòng 44): Ghi rõ quy tắc chuyển đổi CSV `空配列: [] → ""`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 2 (POST) cột Required ghi là No, và sheet データモデル cho phép lưu mảng rỗng [] → ''. Em muốn confirm lại là: Client gửi mảng rỗng [] (không chọn loại hình hoặc công đoạn nào) thì vẫn hợp lệ và tạo được dự án, hay là bắt buộc phải chọn tối thiểu 1 mục ạ? (Team em đề xuất cho phép gửi [] theo đúng Required: No)."*
* **Mentor trả lời:**  
  **"Client gửi mảng rỗng thì vẫn hợp lệ và cho phép tạo dự án"**.

---

#### Q4. Xử lý trùng chữ hoa / thường khi tự động Upsert `tech_tags`
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 2 (`POST /projects`, dòng 59): Constraint ghi `technologies の値は tech_tags テーブルに自動登録（upsert）`.
  * Sheet `API詳細` - Mục 6 (`GET /tech-tags`, dòng 92): Ghi chú tìm kiếm `大文字小文字区別なし` (không phân biệt hoa thường).
  * Sheet `データモデル` (dòng 36): Bảng `tech_tags` cột `name` có constraint `UNIQUE, NOT NULL`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 2 spec yêu cầu tự động upsert tag mới vào bảng tech_tags, và Mục 6 tìm kiếm autocomplete không phân biệt hoa thường. Em muốn confirm là: Khi upsert tag, Backend sẽ so khớp không phân biệt hoa thường (ví dụ 'react' trùng 'React' thì không tạo mới) để tránh rác từ điển tag đúng không ạ? Và khi xóa project thì giữ nguyên các tag trong tech_tags chứ không xóa theo đúng không ạ?"*
* **Mentor trả lời:**  
  **"Khi upsert tag, Backend sẽ so khớp phân biệt hoa thường (ví dụ nếu đã tồn tại 'react' mà có thêm 'React' thì vẫn tạo mới). Khi xóa project thì vẫn giữ nguyên các tag trong tech_tags"**.

---

#### Q5. Logic kết hợp giữa các bộ lọc (Multi-value Filter: AND hay OR?)
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 1 (`GET /projects`, dòng 9-11):
    * `technology`: `技術でフィルタ（OR条件）`
    * `project_type`: `種別でフィルタ（OR条件）`
    * `dev_process_phase`: `開発工程でフィルタ（OR条件）`
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 1 spec ghi rõ trong từng trường là (OR条件). Nhưng khi client truyền nhiều bộ lọc cùng lúc (ví dụ vừa chọn technology vừa chọn project_type) thì giữa các trường với nhau là quan hệ AND đúng không ạ?"*
* **Mentor trả lời:** **Đúng**.

---

#### Q6. Giới hạn cận trên của tham số phân trang `page_size`
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 1 (`GET /projects`, dòng 7): Tham số `page_size` ghi Type: int, Required: No, Default: 20, Description: `1ページあたりの件数`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 1 spec ghi mặc định page_size = 20 nhưng không ghi giá trị tối đa (Max). Để tránh trường hợp client truyền page_size quá lớn làm tràn bộ nhớ và nghẽn DB, Backend có nên giới hạn max = 100 (hoặc chặn validate le=100) không ạ?"*
* **Mentor trả lời:**  
  **"Set giới hạn max = 1000"**.

---

### 2. VỀ AUTH & PHÂN QUYỀN

#### Q7. Vai trò `role` trong bảng `users` và phạm vi tài khoản Admin
* **Vị trí trong Excel:**
  * Sheet `データモデル` (dòng 7): Bảng `users` có cột `role VARCHAR(20) NOT NULL, default='member'`.
  * Sheet `API詳細` - Mục 7 & 8 (dòng 106, 119): API Register cố định trả về `user.role: member`, API Login trả về `user.role`.
* **Câu hỏi confirm với Mentor:**  
  *"Trong bảng users có cột role, nhưng API đăng ký luôn cố định role là member và hệ thống không có API cấp quyền admin. Anh cho em hỏi: Trong bài tập lần này có cần làm tính năng phân quyền riêng cho Admin không ạ?"*
* **Mentor trả lời:**  
  **"Tạm thời chưa cần tính năng phân quyền"**.

---

#### Q8. Thời hạn sống của JWT Token & Refresh Token
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 8 (`POST /auth/login`, dòng 117): Response trả về `idToken | string | JWTトークン`. Không có trường `refresh_token` hay `expires_in`.
  * Sheet `API一覧` (dòng 7-8): Không có endpoint `/auth/refresh`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 8 spec chỉ trả về JWT token mà không có refresh token. Em muốn confirm: Thời hạn sống của token nên để bao lâu ạ? Và khi token hết hạn thì phía Frontend chỉ cần redirect về trang /login để đăng nhập lại, không cần cơ chế Refresh Token đúng không ạ?"*
* **Mentor trả lời:**  
  **"Thời gian sống của token để 24h. Khi token hết hạn thì phía Frontend chỉ cần redirect về trang /login để đăng nhập lại, không cần cơ chế Refresh Token"**.

---

#### Q9. Quyền Sửa/Xóa dự án: Có ràng buộc theo người tạo (`created_by`) không?
* **Vị trí trong Excel:**
  * Sheet `API詳細` - Mục 4 (`PUT /projects/{id}`, dòng 70) & Mục 5 (`DELETE`, dòng 80): Cột Auth đều ghi `Auth: Yes`.
  * Sheet `API詳細` - Mục 2 (`POST /projects`, dòng 55): Response trả về `created_by: 作成者メールアドレス`.
* **Câu hỏi confirm với Mentor:**  
  *"Ở Mục 4 (PUT) và Mục 5 (DELETE) chỉ yêu cầu Auth: Yes (đã đăng nhập). Hệ thống có áp dụng quy tắc 'chỉ người tạo (created_by) mới được sửa/xóa dự án của mình' không, hay bất kỳ ai đăng nhập trong hệ thống cũng đều có quyền sửa/xóa dự án của nhau ạ?"*
* **Mentor trả lời:**  
  **"Bất kỳ ai đăng nhập trong hệ thống cũng đều có quyền sửa/xóa dự án của nhau"**.

---

### 3. VỀ PHẦN DEMO

#### Q10. Chuẩn bị dữ liệu mẫu (Seed Data) cho buổi Demo W12
* **Câu hỏi confirm với Mentor:**  
  *"Để phục vụ buổi nghiệm thu Demo cuối tuần W12 hiển thị tốt tìm kiếm, bộ lọc và phân trang ở Mục 1, team em dự kiến viết sẵn một script seed_data.py nạp sẵn khoảng 15-20 dự án mẫu đa dạng tag/trạng thái vào DB, anh có yêu cầu cụ thể nào về bộ dữ liệu mẫu này không ạ? hay tụi em tự tạo dữ liệu mẫu ạ?"*
* **Mentor trả lời:**  
  **"OK. Team tự tạo dữ liệu mẫu"**.
