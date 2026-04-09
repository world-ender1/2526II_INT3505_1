# Giải Thích: Tại Sao Cursor Nhanh Hơn Offset Trong Phân Trang Sâu (Deep Pagination)?

Qua kết quả chạy thực tế (Benchmark), chúng ta đã thấy **Offset Pagination** mất khoảng ~612ms, trong khi **Cursor Pagination** chỉ mất chưa tới ~2ms. Chậm hơn chênh lệch nhau lên tới hơn 300 lần. Dưới đây là cách giải thích chi tiết nguyên lý hoạt động dẫn đến kết quả này.

---

## 1. Cơ Chế Của Phân Trang Offset (Sử dụng `Skip` / `Limit`)

**Câu lệnh thực thi:** `db.collection.find().skip(999980).limit(20)`

Kỹ thuật phân trang bằng Offset là yêu cầu CSDL *"Bỏ qua 999.980 bản ghi đầu tiên, sau đó lấy ra 20 bản ghi tiếp theo"*.

- **Cách CSDL hoạt động:** MongoDB (và phần lớn các CSDL SQL/NoSQL khác) không hề biết cách "phép thuật" nào để nhảy vọt qua 999.980 bản ghi ngay lập tức. Thay vào đó, bộ máy quét dữ liệu buộc phải đếm và dò từ dòng số `1`, dòng `2`, rà soát tuần tự cho tới dòng thứ `999.980`.
- **Hệ quả:** Dữ liệu càng to (chẳng hạn người dùng càng lật tới các trang sâu), CSDL càng phải hoạt động nặng nhọc để quét qua một lượng dữ liệu rỗng vô ích và vứt bỏ nó đi. Chi phí thuật toán tăng tuyến tính: **$O(N)$**.
- **Điểm yếu phụ:** Hiện tượng *"Data Drift"* (trôi dữ liệu). Nếu quá trình người dùng chuyển trang có một bản ghi mới được sinh ra ở trang 1, toàn bộ số thứ tự nhảy offset sẽ bị đẩy lùi một nhịp, dẫn đến việc người dùng sẽ thấy mình bị đọc lặp lại bản ghi ở trang tiếp theo.

---

## 2. Cơ Chế Của Phân Trang Cursor (Sử dụng `_id ` hoặc `B-Tree Index`)

**Câu lệnh thực thi:** `db.collection.find({ _id: { $gt: last_id_cua_trang_truoc } }).limit(20)`

Kỹ thuật Cursor không bảo DB phải bỏ qua số lượng dòng, mà cung cấp một cái neo (Anchor/Cursor) đánh dấu: *"Hãy tìm dữ liệu bắt đầu ngay đằng sau cái ID này"*.

- **Cách CSDL hoạt động:** Tất cả CSDL thực ra có một tấm bản đồ ẩn gọi là **Index** (Cấu trúc dữ liệu cây B-Tree). Thay vì đếm từng dòng một, CSDL dùng đặc tính tìm kiếm nhị phân của cây B-Tree để tiến hành dò dẫm trên Index, và có thể "định vị" thẳng tới toạ độ ID đó trên cây B-Tree ngay tức khắc (thời gian rất nhỏ, theo thuật toán Logarit **$O(log N)$**). 
- Một khi đã nhảy đúng tới toạ độ đó trên cây B-Tree, CSDL chỉ việc gặt đúng 20 thằng ở bên cạnh nó đi ra là xong!
- **Hệ quả:** Thời gian gần như lúc nào cũng là **hằng số** ở mốc 1 -> 5ms dù bảng dữ liệu có 1 triệu hay 1 tỷ dòng. Bật nhảy đến tận trang 50.000 cũng nhanh y hệt như đang truy xuất trang 1 vậy.
- **Giải quyết Data Drift:** Do tham chiếu bởi một cái ID cứng (chứ không phải vị trí tương đối), dù người ta có xoá hay chèn dòng ở trang 1, toạ độ Cursor ID để bắt đầu ở trang tiếp theo cũng vẫn không bao giờ bị lệch.

---

## 3. Tổng Kết Đánh Giá

| Tiêu Chí | Offset Pagination (`Skip`) | Cursor Pagination (`> ID`) |
|----------|----------------------------|----------------------------|
| **Hiệu năng truy vấn nông (Trang 1-5)** | Rất nhanh (Không có sự khác biệt) | Rất nhanh |
| **Hiệu năng "Deep Pagination" (Trang 1000+)**| Cực chậm. Càng sâu càng chậm (Lag DB) | Vẫn cực kỳ nhanh, ổn định (Flat Time) |
| **Hiện tượng lặp / hụt Item** | Có (Khi data trôi thời gian thực) | Không bao giờ |
| **Độ khó khi code CSDL** | Dễ triển khai | Phải phụ thuộc Index B-Tree / Tìm theo sorting |

➡️ **Kết luận cuối cùng**: Phân trang Offset chỉ nên dùng cho các trang tin tức nhỏ gọn ít thao tác Realtime, còn Cursor (Con trỏ) là công nghệ bắt buộc phải áp dụng đối với tất cả cơ sở dữ liệu Big Data, Mạng Xã Hội có tính năng Infinite Scroll (Cuộn chuột không giới hạn giống hệt như bảng tin Facebook hay Tiktok).
