# Buổi 9: API Versioning và Lifecycle Management

## 1. Mục Tiêu Cần Đạt
- Hiểu các chiến lược versioning: URL, header, query param.
- Biết cách xử lý breaking changes và deprecation cho API.
- Triển khai được versioning cho API trong thực tế (ví dụ: `/api/v1/users` → `/api/v2/users`).
- Lập được kế hoạch nâng cấp API (migration plan).

---

## 2. Các Nội Dung Code Cần Demo

Để minh họa các khái niệm trên, buổi học sẽ demo một số đoạn code xoay quanh **Payment API (API Thanh toán)**:

### 2.1. Demo 3 Chiến Lược Versioning
- **URL Versioning:** Định tuyến các request có version được nhúng trực tiếp trong URL (VD: `/api/v1/payments` và `/api/v2/payments`).
- **Query Parameter Versioning:** Lấy version từ query string để quyết định logic xử lý (VD: `/api/payments?version=1`).
- **Header Versioning (Content Negotiation):** Nhận version từ Custom Header do client gửi lên (VD: `X-API-Version: 1` hoặc header `Accept`).

### 2.2. Demo Quản Lý Lifecycle (Deprecation & Breaking Changes)
- Thêm HTTP headers chuẩn (`Deprecation`, `Sunset`, `Link`) vào response của API v1 để cảnh báo developer rằng API này sắp bị dừng hoạt động.

### 2.3. Case Study Thực Hành: Thiết kế chiến lược nâng cấp từ v1 sang v2
- **Code API v1 (Legacy):** API nhận một payload đơn giản. VD: `{ "amount": 100, "currency": "USD" }`.
- **Code API v2 (Mới):** API có payload phức tạp hơn (Breaking Change). VD: gộp `amount` và `currency` vào một object `price`, bắt buộc có `payment_method`.

---

## 3. Các Bước Làm (Demo Steps)

Giảng viên/Sinh viên thực hiện các bước sau trong quá trình demo trên lớp:

### Bước 1: Khởi tạo Project & API v1 (Payment API Legacy)
1. Thiết lập một ứng dụng backend cơ bản (sử dụng Flask/ExpressJS/FastAPI).
2. Xây dựng route `POST /api/v1/payments`.
3. Viết logic xử lý thanh toán nhận payload dạng phẳng (`amount`, `currency`).
4. Chạy server, sử dụng Postman gửi request để test API v1.

### Bước 2: Hiện thực API v2 với Breaking Changes (URL Versioning)
1. Xây dựng route `POST /api/v2/payments` hoạt động song song với v1.
2. Viết logic yêu cầu payload mới cấu trúc lồng nhau (nested object) và thêm trường bắt buộc mới.
3. Dùng Postman gửi request chuẩn v2 và so sánh sự khác biệt.

### Bước 3: Triển khai các phương thức Versioning khác
1. **Query Param:** Tạo một route chung `POST /api/payments`. Đọc tham số `?v=1` hoặc `?v=2` để gọi hàm controller tương ứng. Test bằng Postman.
2. **Header Versioning:** Tiếp tục sửa route chung để ưu tiên đọc header `X-API-Version`. Nếu client truyền `X-API-Version: 2`, gọi logic v2. Dùng Postman cấu hình header để test.

### Bước 4: Viết Thông báo Deprecation & Kế hoạch nâng cấp
1. **Tạo tài liệu (Migration Plan):** Viết nhanh một file markdown (hoặc API Doc) hướng dẫn dev chuyển đổi payload từ v1 sang v2.
2. **Cập nhật code API v1 để thêm Deprecation Headers:**
   - Thêm header `Deprecation: true`.
   - Thêm header `Sunset: <Ngày giờ đóng cửa API>`.
   - Thêm header `Link: <URL_tới_Migration_Plan>; rel="deprecation"`.
3. Chạy test lại API v1 bằng Postman, mở tab Headers của response để cho sinh viên thấy rõ các thông báo deprecation được trả về cho client như thế nào.

---

## 4. Tài Liệu Đọc Trước
- **James Higginbotham – Chương 8**: Đọc để hiểu sâu về lý thuyết thiết kế API theo vòng đời, các nguyên lý về backward compatibility và khi nào thì nên bắt đầu làm version 2.
