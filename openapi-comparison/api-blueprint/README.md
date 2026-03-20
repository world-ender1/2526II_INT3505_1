# API Blueprint Demo: Library Management

Thư mục này chứa mô tả API Quản lý Thư viện viết bằng định dạng **API Blueprint** (MSON - Markdown Syntax for Object Notation).

## 1. Ưu điểm nổi bật

API Blueprint sử dụng Markdown, khiến nó trở thành công cụ cực kỳ dễ đọc ngay cả đối với Project Manager, QA hay Business Analyst. Nó tập trung vào việc mô tả Document-first.

## 2. Hướng dẫn Test API tự động (Code Generation / Flow Testing)

Một trong những công cụ mạnh mẽ nhất của hệ sinh thái Blueprint là **Dredd**. Thay vì sinh code server, Dredd tự động parse file Markdown này và biến thành một loạt các **integration test cases** để tự tìm đến Server gốc và gọi thử.

### Yêu cầu
Cài đặt Node.js và NPM.
Cài đặt công cụ Dredd global:
```bash
npm install -g dredd
```

### Cách Test (Sinh Test)
Giả sử bạn đã code xong Server API Library bằng Flask hoặc ExpressJS (chạy ở cổng 5000: `http://localhost:5000`).

**Bước 1**: Mở terminal tại thư mục `api-blueprint` này.

**Bước 2**: Khởi tạo cấu hình Dredd
```bash
dredd init
```

**Bước 3**: Chạy Test
```bash
dredd api.apib http://localhost:5000
```
Dredd sẽ tự động đi qua tất cả các endpoint bạn mô tả trong `api.apib`: 
- Nó lấy mẫu gửi đi (Ví dụ Body POST `/books`).
- Gửi thực tế đến localhost:5000.
- Nó so sánh Output Model của server đối chiếu với Output Model (Response 200, 201) trong file Markdown.
- Báo XANH (Pass) hoặc ĐỎ (Fail). 

Đây là **Contract-driven Testing** hoàn toàn không cần viết code unit test thủ công.
