# Kịch Bản Chạy Demo Trên Lớp (Tuần 5)

Để phần demo trên lớp diễn ra suôn sẻ, bạn hãy mở 2 phần mềm: **VSCode** (để gõ lệnh Terminal) và **Trình duyệt Web** (Hoặc Postman) để chứng minh kết quả. Bạn cứ làm chậm rãi theo 4 bước sau:

## Bước 1: Giới thiệu & Khởi tạo dữ liệu trực tiếp
Mở Terminal trong thư mục `d:\soa\week5hw` và gõ lệnh sau trước mặt lớp:
```bash
python seed.py
```
> **Bạn nói gì lúc này:** *"Thưa thầy và các bạn, để bài Test công bằng, em xin phép xóa toàn bộ Database cũ và trực tiếp tạo ra 1.000.000 dòng dữ liệu Log ngẫu nhiên vào hệ thống MongoDB. Quá trình này dùng bulk insert nên chỉ mất vài giây..."*

*(Chờ 8 giây để tool chạy xong 100% lô và báo thành công).*

## Bước 2: Bật Server API
Gõ tiếp lệnh sau vào Terminal để khởi chạy Backend:
```bash
python app.py
```
> **Bạn nói gì lúc này:** *"Bây giờ em đã bật Server Flask chạy ngầm ở cổng 5000 để quản lý 2 endpoint thử nghiệm phân trang."*

## Bước 3: Phô diễn sự chậm chạp của Offset Pagination
Mở trình duyệt Web (Chrome/Edge), phóng to màn hình. 
Đầu tiên, bạn vào nhanh trang 49.999 để lấy ID làm mốc:
👉 `http://127.0.0.1:5000/api/offset?page=49999`
*Lưu ý thao tác: Kéo xuống dưới cùng, bôi đen dòng chữ `_id` của bản ghi cuối cùng trong danh sách và copy lại.*

Tiếp theo, bạn gõ đường dẫn lật sang trang thứ 50.000 (trang chúng ta cần demo):
👉 `http://127.0.0.1:5000/api/offset?page=50000`

> **Bạn nói gì lúc này:** *"Bây giờ em sẽ lật tới trang thứ 50.000 bằng phương pháp cũ (Method Offset). Hãy chú ý dòng chữ `execution_time_ms`. MongoDB mất tới hơn 600ms (nửa giây) rât chậm. Lý do là vì nó phải quét và đếm bỏ chạy rỗng từ bản ghi số 1 tới điểm 999.980."*

## Bước 4: Cú chốt (Phô diễn tốc độ khủng khiếp của Cursor với cùng kết quả)
Mở một tab trình duyệt khác để so sánh, dán đường dẫn API Cursor trỏ đúng vào ID của trang 49.999 bạn vừa copy ban nãy:
👉 `http://127.0.0.1:5000/api/cursor?cursor_id=<ID_VỪA_COPY>`

> **Bạn nói gì lúc này:** *"Bây giờ thay vì đếm chay, em sẽ dùng phương pháp Cursor. Em lấy toạ độ ID của thằng cuối cùng của trang trước đó làm cột mốc. CSDL giờ đây đi thẳng vào cây B-Tree Index và xuất kết quả trang 50.000 ra ngay lặp tức (dữ liệu giống hệt bên Offset). Xin thầy và lớp nhìn vào chỉ số `execution_time_ms`."*

*(Kết quả hiển thị trên màn hình trình duyệt lúc này sẽ chỉ là `1.2ms`, nhanh hơn gấp vài trăm lần, và danh sách records hoàn toàn trùng khớp với tab bên kia).*

---
**Kết luận bài thuyết trình:** *"Qua bài tập này, em nhận thấy khi dữ liệu lớn, việc đánh Index (B-Tree) và sử dụng Cursor Pointer mang lại độ ổn định thời gian tuyệt đối (hằng số), giải quyết triệt để rủi ro nghẽn cổ chai của các hệ thống như Mạng Xã Hội."*
