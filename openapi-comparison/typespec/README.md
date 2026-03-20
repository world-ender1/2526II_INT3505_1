# TypeSpec Demo (bởi Microsoft): Library Management

Thư mục này chứa file mô tả API Quản lý Thư viện viết bằng ngôn ngữ **TypeSpec**.

## 1. Ưu điểm nổi bật của TypeSpec

TypeSpec không dùng YAML hay Markdown, mà nó là một **ngôn ngữ lập trình (DSL) có cú pháp rất giống TypeScript**. 
Điều này cung cấp trải nghiệm Developer cực tốt vì:
- Bắt lỗi cú pháp, type-checking ngay trong VSCode (qua extension).
- Khai báo Class (Models/Interfaces) thay vì Schema thô cứng.
- Không sợ lỗi thụt lề (indentation) như YAML.

## 2. Compilation (Compiler generation)

TypeSpec thực tế đóng vai trò như một bộ mã nguồn (Source code), nó chưa thể được Backend hay Frontend hiểu ngay. Bạn **bắt buộc phải Compile (Biên dịch)** TypeSpec ra chuẩn trung gian như **OpenAPI 3.0** hay JSON Schema.

### Yêu cầu
Cài đặt Node.js / NPM.
Cài đặt trình biên dịch TypeSpec và module OpenAPI3:
```bash
npm install -g @typespec/compiler
npm install @typespec/openapi3
```

### Cách thức sinh ra Code / OpenAPI yaml

**Bước 1**: Mở terminal tại thư mục `typespec` này.

**Bước 2**: Biên dịch file `main.tsp` ra file chuẩn OpenAPI:
```bash
tsp compile main.tsp --emit @typespec/openapi3
```

**Bước 3**: Sau khi chạy lệnh trên, TypeSpec sẽ tạo ra thư mục `tsp-output/`. Bên trong đó sẽ có file `openapi.yaml`. File này **chính là** OpenAPI spec chuẩn công nghiệp.

**Bước 4**: Bước tiếp theo, bạn lấy chính file `openapi.yaml` vừa sinh ra đó để chạy vào công cụ mã nguồn chung (ví dụ `swagger-codegen`, `openapi-generator` như ở thư mục `/openapi`) để biến nó thành Server Code Web App (C#, Python, Node) hoặc Client Code, Mock Server.

*Kết luận: Dùng TypeSpec biến quá trình viết YAML nhàm chán của OpenAPI thành một trải nghiệm "viết code API" nhàn nhã hơn nhiều cho lập trình viên.*
