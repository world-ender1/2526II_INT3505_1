# Hướng Dẫn Nâng Cấp API Thanh Toán (Migration Guide)

## 1. Tổng Quan
Payment API v1 đã chính thức **bị deprecate (đánh dấu lỗi thời)** và sẽ ngừng hoạt động (Sunset) vào ngày **31/12/2026**. 
Chúng tôi khuyến nghị tất cả các nhà phát triển (developers) nâng cấp lên **Payment API v2** càng sớm càng tốt để tận dụng các tính năng bảo mật và phương thức thanh toán mới.

## 2. Các Thay Đổi Chính (Breaking Changes)

API v2 thiết kế lại cấu trúc payload của Request. Cụ thể:
1. Trường `amount` và `currency` không còn nằm ở thư mục gốc (root) của JSON object, mà được gom vào trong một object mới tên là `price`.
2. Bắt buộc phải cung cấp tham số `payment_method` (phương thức thanh toán).

## 3. So Sánh Payload

### API v1 (Legacy) - Sắp ngừng hoạt động
**Endpoint:** `POST /api/v1/payments`

```json
{
  "amount": 100,
  "currency": "USD"
}
```

### API v2 (Mới nhất)
**Endpoint:** `POST /api/v2/payments`

```json
{
  "price": {
    "amount": 100,
    "currency": "USD"
  },
  "payment_method": "credit_card"
}
```

## 4. Hướng Dẫn Chuyển Đổi (Client/Frontend)
- Cập nhật URL endpoint gọi API từ `/api/v1/payments` thành `/api/v2/payments`. 
- *(Hoặc, nếu đang dùng header/query versioning, đổi `X-API-Version` thành `2`, hoặc query `?v=2`)*.
- Cập nhật logic tạo request body theo cấu trúc JSON của v2.

Nếu bạn gặp khó khăn trong quá trình nâng cấp, vui lòng liên hệ đội ngũ hỗ trợ API.
