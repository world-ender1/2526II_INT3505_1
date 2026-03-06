# Demo Uniform Interface trong REST

Project này dùng Flask để minh hoạ ràng buộc **Uniform Interface** của REST.

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

## Chạy demo

1. Cài thư viện:
   - `pip install flask requests`
2. Chạy server:
   - `python server.py`
3. Mở terminal khác, chạy client:
   - `python client.py`

Client sẽ lần lượt gọi các API để bạn trình bày đầy đủ Uniform Interface.
