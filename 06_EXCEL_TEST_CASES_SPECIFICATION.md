# 06. PHÂN CHIA VIẾT TEST CASE EXCEL CHO 3 THÀNH VIÊN (TUẦN W11)
## Bảng Phân Công 6 Sheet Kiểm Thử Giao Diện Theo Form Mẫu Của Mentor

**Dự án:** プロジェクト管理システム (Project Performance Management System)  
**Thời gian thực hiện:** **Tuần W11** (Viết kịch bản vào file Excel mẫu của Mentor và chạy test trực tiếp trên giao diện React)  
**Quy cách thực hiện:** Dựa trên mẫu sheet `検査項目一覧／成績表` có sẵn của Mentor, mỗi thành viên sẽ tự phụ trách viết kịch bản test và đánh dấu kết quả (`○` Pass / `×` Fail) cho **đúng 2 màn hình/sheet** được phân công.

---

## 👥 1. BẢNG PHÂN CHIA MÀN HÌNH CHO 3 THÀNH VIÊN

| Thành viên | Tên Sheet trong Excel | Màn hình / Chức năng phụ trách | Phạm vi nghiệp vụ cần kiểm thử |
| :--- | :--- | :--- | :--- |
| 👑 **Long** | **1. `ログイン画面-UI確認`** | Màn hình Đăng nhập (`/login`) | - Giao diện form đăng nhập, placeholder.<br>- Validate bỏ trống email/password.<br>- Đăng nhập thành công (200) $\rightarrow$ lưu JWT token, redirect `/projects`.<br>- Đăng nhập thất bại (401) $\rightarrow$ thông báo tiếng Nhật. |
| | **2. `ユーザー登録画面-UI確認`** | Màn hình Đăng ký (`/register`) & Điều hướng | - Giao diện form đăng ký, validate mật khẩu từ 8–100 ký tự.<br>- Validate khớp mật khẩu xác nhận.<br>- Đăng ký thành công (201) $\rightarrow$ tự động lưu token và chuyển trang.<br>- Chặn trùng email (409).<br>- `RouteGuard` chặn URL khi chưa login và nút Đăng xuất (`ログアウト`). |
| 📊 **Khanh** | **3. `プロジェクト一覧画面-UI確認`** | Màn hình Danh sách dự án (`/projects`) | - Hiển thị bảng dữ liệu, ánh xạ các cột từ CSDL.<br>- Hiển thị trạng thái dự án đang diễn ra (`進行中`).<br>- Chuyển đổi giữa 2 chế độ xem: Dạng bảng (Table) và Dạng thẻ (Card).<br>- Phân trang `< 1 2 3 >` (nút Trước/Sau, hiển thị số trang).<br>- Trạng thái 0 bản ghi (0件表示: `"該当するプロジェクトが見つかりません"`).<br>- Ẩn hoàn toàn các dự án đã xóa mềm (`deleted_at IS NOT NULL`). |
| | **4. `検索・フィルター機能-UI操作`** | Tìm kiếm `q`, Bộ lọc đa điều kiện & Paging | - Thanh tìm kiếm toàn văn `q` (debounce 300ms / phím Enter).<br>- 3 Dropdown lọc: Loại hình (`project_type`), Công đoạn (`dev_process_phase`), Công nghệ (`technology`).<br>- Logic lọc: **OR trong cùng 1 field, AND giữa các field** (theo Q5 Mentor).<br>- Hiển thị chip lọc đang chọn, nút xóa từng chip và nút xóa tất cả filter. |
| 🏷️ **Tuyết** | **5. `プロジェクト作成画面-UI確認`** | Màn hình Tạo mới (`/projects/new`) | - Giao diện Form nhập đủ 18 fields theo từng nhóm.<br>- Validate bắt buộc nhập: Tên khách hàng, Tên dự án, Ngày bắt đầu.<br>- Validate ngày kết thúc $\ge$ ngày bắt đầu.<br>- Tích chọn `is_ongoing = True` $\rightarrow$ vô hiệu hóa ô ngày kết thúc (chặn lỗi 422).<br>- Dropdown Autocomplete gợi ý tag (không phân biệt hoa/thường, max 20 tag).<br>- Thêm tag công nghệ mới chưa có trong DB. |
| | **6. `プロジェクト詳細・編集・削除-UI確認`** | Màn hình Chi tiết (`/projects/:id`), Chỉnh sửa & Xóa mềm | - Xem chi tiết đầy đủ 18 fields, các chip Badge màu sắc.<br>- Nút `編集` $\rightarrow$ chuyển sang `/projects/:id/edit`, pre-fill dữ liệu cũ vào form.<br>- Cập nhật dự án thành công, đồng bộ lại tag.<br>- Nút `削除` $\rightarrow$ mở Modal popup xác nhận xóa mềm.<br>- Xóa mềm thành công: Dự án biến mất khỏi danh sách, link chi tiết báo 404.<br>- Giữ nguyên các tag trong `tech_tags` sau khi xóa dự án (theo Q4 Mentor). |

---
