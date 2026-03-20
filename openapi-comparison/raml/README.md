# RAML Demo: Library Management

Thư mục này chứa mô tả API Quản lý Thư viện viết bằng ngôn ngữ **RAML 1.0** (RESTful API Modeling Language).

## 1. RAML vs OpenAPI

RAML sử dụng YAML, nó rất giống với OpenAPI nhưng nổi bật bởi cấu trúc cây tuyến tính hơn cho các Resource (`/books` rồi lùi vào để định nghĩa Method, thay vì OpenAPI định nghĩa theo `paths -> methods`). 
Bên cạnh đó, RAML hỗ trợ mạnh mẽ Data Types, Traits (các behavior tái sử dụng giống nhau ở nhiều endpoint) để duy trì quy tắc DRY (Don't Repeat Yourself).

## 2. Hướng dẫn Code Generation 

Bạn có thể sinh code trực tiếp từ file `api.raml` này ra các dạng Node.js Express, Java Spring, hoặc Client SDK bằng công cụ **osprey** hoặc **ramlio**.

Ví dụ tạo **Mock Middleware Server** nhanh từ file RAML để Front-end có thể dùng tạm (không cần dev Backend code):

### Yêu cầu
Cài đặt Node.js / NPM.
Cài đặt công cụ osprey-mock-service:
```bash
npm install -g osprey-mock-service
```

### Cách chạy Mock Server
**Bước 1**: Mở terminal tại thư mục `raml`

**Bước 2**: Chạy Mock server dựa trên file `.raml`
```bash
osprey-mock-service -f api.raml -p 3000
```
Server sẽ được kích hoạt tại `http://localhost:3000`. Osprey sẽ tự động đọc schemas và `example` JSON trong `api.raml` để trả về dữ liệu ảo mỗi khi ta gọi:
```bash
curl http://localhost:3000/v1/books
```
Điều này đem lại khả năng code độc lập (Decoupled Generation) cực mạnh.
