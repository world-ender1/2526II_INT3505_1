# Demo REST: Uniform Interface + Stateless

Project này dùng Flask để minh hoạ 2 ràng buộc của REST: **Uniform Interface** và **Stateless**.

## 1) Resource-based URI

- Collection: `/tasks`
- Item: `/tasks/{id}`

URI chỉ biểu diễn tài nguyên (danh từ), không nhúng hành động như `/createTask`.

## 2) Dùng chuẩn HTTP methods

- `GET /tasks`: lấy danh sách task
- `POST /tasks`: tạo task mới
- `GET /tasks/{id}`: lấy 1 task
- `PUT /tasks/{id}`: thay toàn bộ task
- `PATCH /tasks/{id}`: cập nhật một phần task
- `DELETE /tasks/{id}`: xoá task

## 3) Self-descriptive messages

- Request/response dùng JSON
- Trả status code đúng ngữ nghĩa: `200`, `201`, `204`, `400`, `404`

## 4) HATEOAS (liên kết trong representation)

Mỗi task trả về có `links.self` và `links.collection` để client biết các bước tiếp theo.

## 5) Stateless (không lưu session phía server)

- Server **không lưu trạng thái đăng nhập/session** của client.
- Mỗi request đến `/tasks` phải tự mang đủ thông tin qua header `X-Client-Id`.
- Nếu thiếu header này, server trả `400`.
- Response trả lại `client_id` để thấy rõ request nào đang được xử lý.

## Chạy demo

1. Cài thư viện:
   - `pip install flask requests`
2. Chạy server:
   - `python server.py`
3. Mở terminal khác, chạy client:
   - `python client.py`

Client hiện demo 1 request `GET /tasks` và gửi `X-Client-Id` để thể hiện Stateless.
