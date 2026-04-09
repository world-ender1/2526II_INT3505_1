# Báo Cáo Học Thuật: JWT Authentication và Bảo Mật (Tuần 2)

Dưới đây là phần trình bày lý thuyết theo yêu cầu của giáo trình môn kiến trúc Web/SOA.

## I. So sánh JWT với OAuth 2.0
Một lỗi nhận thức phổ biến là xem **JWT** và **OAuth 2.0** như hai công nghệ cạnh tranh (có thể thay thế nhau). Tuy nhiên, chúng gỡ quyết hai bài toán khác hẳn nhau và thường được "mix" lại với nhau:

1. **OAuth 2.0 (Giao thức Uỷ quyền - Authorization Protocol)**: OAuth 2.0 là một bộ quy tắc (Khung kiến trúc) quy định CÁCH THỨC thiết bị ngoài (Third-party) xin phép người dùng để mượn chìa khóa truy cập vào Facebook/Google của họ mà không cần đưa tên đăng nhập hay mật khẩu.
2. **JWT (Chuẩn định dạng thẻ chữ ký - Token Format)**: JWT (JSON Web Token) đơn thuần là MỘT ĐỊNH DẠNG sinh ra tấm thẻ chìa khóa chứa thông tin (Ví dụ: thẻ ghi tên ai, cấp ngày nào, có ai ký xác nhận). 
3. **Mối quan hệ:** Khi chạy theo quy trình chuẩn của OAuth 2.0, điểm cuối cùng server cấp cho App bên thứ 3 một cái "Access Token". Bản thân cái Access Token đó thường được mã hóa, gói bọc dưới định dạng **JWT**! OAuth 2.0 là con đường để xin xỏ, JWT là tấm thẻ để đi đường.

## II. Các Khái Niệm Quan Trọng

### 1. Bearer Token
"Bearer" có nghĩa là *kẻ cầm đồ / người mang theo*. 
Bearer Token hiểu đơn giản là tấm vé vô danh. **Bất cứ ai** kẹp tấm vé này trên đầu tay (Header `Authorization: Bearer <token>`) là hệ thống mặc định coi người đó chính là chủ nhân. Nó vừa tiện lợi (Stateless - không cần ghi sổ server), vừa rủi ro. Vì lỡ hacker đánh cắp được token (Token Leakage), họ nghiễm nhiên trở thành chủ nhân.

### 2. Refresh Token
Do tính chất của Bearer Token bị đánh cắp rất nguy hiểm (Replay Attack), ta buộc phải ép Access Token **chỉ được xài trong khoảng thời gian rất ngắn** (ví dụ 15 - 30 phút).
Mỗi lần hết hạn, thay vì bắt khách hàng nhập lại Tên đăng nhập và Mật khẩu, hệ thống sinh thêm một mã **Refresh Token** (có hạn rất dài: 30 ngày) được giấu kín. Hệ thống Front-end sẽ cầm Refresh Token này lên xin lại Access Token mới. Nếu Refresh Token bị lộ, Backend hoàn toàn có quyền xóa nó khỏi Database ngay lập tức (Blacklist).

### 3. Roles và Scopes
- **Roles (Vai trò)**: Đại diện cho *tư cách* của người dùng trong hệ thống (Ví dụ: `admin`, `moderator`, `user`).
- **Scopes (Phạm vi giới hạn)**: Đại diện cho *những hành động mờ* mà tấm Token có thể làm. (Ví dụ Token cấp cho App theo dõi sức khoẻ chỉ có scope `read:heart_rate`, chứ không có quyền `write:post_facebook`). Việc nhúng Scope ngay vào Token giúp các microservice hạn chế tác hại nếu Token bị hack.

## III. Phân tích Rủi Ro & Đề xuất Khắc phục Bảo mật

Sau quá trình Security Audit cho hệ thống Server bằng Flask hiện tại, tôi đã phát hiện và đề xuất chắp vá các cấu trúc sau:

| Rủi Ro Phát Hiện ở Mã Cũ | Khái Niệm Lỗi (CVE) | Giải Pháp Khắc Phục Lập Trình |
|--------------------------|---------------------|-------------------------------|
| `JWT_SECRET` bị ghi cứng trong Text. | Hardcoded Secrets, Token Leakage | Đưa key vào tệp cấu hình ẩn `.env` hoặc hệ thống quản lý môi trường (Environment Variables). |
| Có hàm tự viết mã hóa bằng `hmac`. | Roll-your-own Crypto | Áp dụng bắt buộc bộ thư viện chống tấn công vét cạn và xác thực chuẩn mã số Quốc Tế (`PyJWT`). |
| Kẻ gian đánh cắp JWT và gửi lại liên tục. | Replay Attack | Nhúng cờ **`jti` (JWT ID)** duy nhất vào Payload, nếu thấy 1 `jti` gửi bất thường lên thì Reject. Rút ngắn TTL vòng đợi của Access token xuống còn 15 phút.
| Mất trải nghiệm người dùng vì phải Log-in lại liên tục khi rút TTL. | UX Disruption / Lack of Extensibility | Xây dựng thêm một cổng `/auth/refresh` và cấp phát một `Refresh Token` trả ngược về HttpOnly Cookie đính kèm. |
