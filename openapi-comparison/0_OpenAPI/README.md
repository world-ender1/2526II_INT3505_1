# OpenAPI Demo: Library Management

Thư mục này chứa file mô tả API Quản lý Thư viện bằng chuẩn **OpenAPI Specification 3.0**.

## 1. File tham chiếu
- `openapi.yaml`: Chứa toàn bộ định nghĩa API (Endpoints, Schemas, Parameters).

## 2. Hướng dẫn Code Generation (Sinh Code)

OpenAPI nổi tiếng nhất với khả năng sinh code tự động ra hàng chục ngôn ngữ khác nhau nhờ công cụ `swagger-codegen` hoặc `openapi-generator-cli`.

### Yêu cầu
- Đã cài đặt Java (JRE/JDK 11+).
- Cài đặt công cụ [OpenAPI Generator CLI](https://openapi-generator.tech/docs/installation):
  ```bash
  npm install @openapitools/openapi-generator-cli -g
  ```

### Các bước thực hiện sinh Flask Server (Python)

**Bước 1**: Mở terminal tại thư mục `openapi` này.

**Bước 2**: Chạy lệnh sinh code cho server Python Flask:
```bash
openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-server
```

**Bước 3**: Chạy server vừa sinh ra
```bash
cd generated-server
pip install -r requirements.txt
python -m openapi_server
```
Sau đó truy cập `http://localhost:8080/ui/` để xem giao diện Swagger UI tự động được tạo ra từ server (giống hệt cách chúng ta làm với project Vercel trước đó).

### Các bước thực hiện sinh Frontend API Client (TypeScript/Axios)

Tương tự, bạn có thể sinh bộ thư viện gọi API cho Frontend ứng dụng Angular/React:
```bash
openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./generated-client
```
Lúc này trong `generated-client` sẽ chứa sẵn các hàm gọi API axios như `Configuration`, `BooksApi().addBook(book)` chuẩn type TypeScript lấy từ `openapi.yaml`. Mọi lỗi type sẽ được Frontend phát hiện ngay từ lúc biên dịch!
