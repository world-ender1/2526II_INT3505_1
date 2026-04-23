# Kịch Bản Demo: API Testing & Quality Assurance (Tuần 8)

Tài liệu này là kịch bản từng bước (step-by-step) để bạn vừa thực hành vừa trình bày cho thầy cô xem về nội dung chương 8: Kiểm thử API và Đảm bảo chất lượng.

---

## 🛠 Chuẩn Bị Trước Khi Demo (Quan Trọng)

Trước khi gọi thầy cô chấm, hãy đảm bảo bạn đã:
1. Mở Terminal (PowerShell) và cài đặt thư viện: `pip install -r requirements.txt`
2. Cài đặt Newman (nếu đã cài Node.js): `npm install -g newman`
3. Bật sẵn API Server chạy ngầm ở 1 Terminal:
   ```bash
   python app.py
   ```
4. Bật sẵn Postman và chuẩn bị 5 endpoints đã có code Test (theo hướng dẫn ở file `API_TESTING_DEMO.md`).

---

## 🎤 Các Bước Trình Bày

### Bước 1: Giới thiệu API và Khái niệm Unit/Integration Testing (3 Phút)
* **Thao tác:** Mở file `app.py` và Postman.
* **Lời thoại gợi ý:** 
  > "Chào thầy/cô, để thực hiện nội dung Chương 8 về API Testing, em đã xây dựng một RESTful API đơn giản quản lý Sản phẩm bằng Flask. Thay vì chỉ dùng Postman để gọi API thủ công, em đã tích hợp **Unit Test** và **Integration Test** trực tiếp vào tab `Tests` của Postman."
* **Thao tác:** Mở request `GET /products` trong Postman, chuyển sang tab **Tests**.
* **Lời thoại gợi ý:**
  > "Ví dụ với API lấy danh sách sản phẩm, em dùng mã JavaScript để tự động kiểm tra 3 thứ: (1) Status code có trả về đúng 200 không, (2) Thời gian phản hồi (Response time) có dưới 200ms không, và (3) Dữ liệu trả về có đúng cấu trúc mảng JSON hay không."
* **Thao tác:** Bấm **Send** và mở mục **Test Results (3/3)** cho thầy cô xem các test case hiện màu xanh (Pass).

### Bước 2: Tự động hóa kiểm thử bằng CLI (Newman) (2 Phút)
* **Thao tác:** Mở một Terminal mới (chưa chạy code).
* **Lời thoại gợi ý:**
  > "Khi làm dự án thực tế với hàng trăm API, việc click chuột chạy từng cái rất mất thời gian. Vì vậy em sử dụng công cụ **Newman** để tự động chạy toàn bộ bộ Test (Test Suite) qua môi trường dòng lệnh (CLI), rất phù hợp để tích hợp vào CI/CD."
* **Thao tác:** Chạy lệnh sau trên terminal (Giả sử bạn đã export collection từ Postman ra tên là `collection.json`):
  ```bash
  newman run collection.json
  ```
* **Lời thoại gợi ý:**
  > "Như thầy/cô thấy, Newman tự động gửi tuần tự cả 5 request CRUD và in ra kết quả pass/fail dạng bảng cực kỳ trực quan trên terminal."

### Bước 3: Kiểm thử Hiệu Năng và Chịu Tải (Load Testing) (3 Phút)
* **Thao tác:** Mở file kịch bản `locustfile.py`.
* **Lời thoại gợi ý:**
  > "Phần tiếp theo của chương là Đo hiệu năng API (Performance Testing). Em sử dụng công cụ **Locust** được viết bằng Python. File script này định nghĩa kịch bản mô phỏng hành vi người dùng thật: họ sẽ có xu hướng gọi API xem danh sách (GET) nhiều gấp 3 lần API tạo mới (POST)."
* **Thao tác:** Chạy lệnh khởi động Locust trên Terminal:
  ```bash
  locust -f locustfile.py
  ```
* **Lời thoại gợi ý:**
  > "Khi em chạy Locust, nó sẽ cung cấp một giao diện web UI để ta điều khiển và theo dõi quá trình tấn công (tạo tải) lên server."

### Bước 4: Trực quan hóa và Báo cáo Hiệu Năng (2 Phút)
* **Thao tác:** Mở trình duyệt, truy cập `http://localhost:8089`.
* **Lời thoại gợi ý:**
  > "Đây là giao diện của Locust. Em sẽ cấu hình mô phỏng **500 người dùng truy cập đồng thời** (Number of users), tốc độ tăng là **10 người/giây** (Spawn rate). Địa chỉ server em đang chạy là `http://localhost:5000`."
* **Thao tác:** Bấm **Start swarming**. Chuyển sang tab **Charts**.
* **Lời thoại gợi ý (Chỉ vào các biểu đồ):**
  > "Ở đây em muốn báo cáo 3 chỉ số quan trọng nhất của Quality Assurance:
  > 1. **RPS (Requests per Second):** Thể hiện server API của em đang xử lý được bao nhiêu truy vấn trong 1 giây.
  > 2. **Response Times (ms):** Nếu đường màu vàng (95th percentile) đi ngang tức là server ổn định. Nếu nó vút lên cao nghĩa là server đang bị nghẽn do quá tải.
  > 3. **Error Rate:** Nếu server quá tải không chịu nổi, các request sẽ trả về lỗi, biểu đồ lỗi này sẽ nhích lên."
* **Kết luận:**
  > "Thông qua Postman và Newman, em đảm bảo API chạy ĐÚNG (Quality). Thông qua Locust, em đảm bảo API chạy KHỎE (Performance). Em xin kết thúc bài demo tuần 8."
