# Hướng Dẫn Thực Hành: Triển Khai Backend Python/Flask với MongoDB từ OpenAPI

Tài liệu này tổng hợp toàn bộ các bước để biến một file thiết kế `api.yaml` thành một Backend ứng dụng đa tính năng, thao tác trực tiếp với cơ sở dữ liệu MongoDB bằng Python/Flask, và cách kiểm thử toàn diện ứng dụng này.

---

## Bước 1: Khởi tạo mã nguồn (Codegen) từ OpenAPI

Từ tệp thiết kế `api.yaml` đã có, chúng ta sẽ bắt máy tự động viết phần thiết lập lõi (Routing, Server, Model rỗng).

> **Làm thế nào?**  
> Mở Terminal và di chuyển vào thư mục dự án `week71`, tiến hành gõ lệnh:
> ```bash
> npx @openapitools/openapi-generator-cli generate -i api.yaml -g python-flask -o .
> ```
*   `-g python-flask`: Ấn định thư viện sinh code (generator) là Python phối hợp với framework Flask.
*   Lệnh sẽ sinh ra toàn bộ tệp cấu trúc gồm `requirements.txt` và lõi source code ở thư mục `openapi_server`.

---

## Bước 2: Chuẩn bị môi trường & Cài đặt thư viện

Để đảm bảo các gói Python cài đặt không bị xung đột với hệ thống máy chủ thật của bạn, hãy tạo "Môi trường ảo (virtual environment)":

1. **Tạo môi trường lấy tên là `venv`:**
   ```bash
   python -m venv venv
   ```
2. **Kích hoạt không gian làm việc này lên:**
   ```bash
   .\venv\Scripts\Activate
   ```
3. **Cài đặt những framework cần thiết & MongoDB Driver:**
   Ta cần cài các thư viện `openapi-generator` đã nhắc tới trong `requirements.txt`, và thư viện `pymongo` chịu trách nhiệm tương tác với Database.
   ```bash
   pip install -r requirements.txt pymongo
   ```

---

## Bước 3: Kết nối Backend với Cơ sở dữ liệu MongoDB

Theo cấu trúc mặc định, nơi có thẩm quyền sửa đổi tương tác Database là những "Bộ điều khiển" - Controllers. 

Mở file: `openapi_server/controllers/default_controller.py`.  
Ta sẽ gắn MongoDB vào ngay phần đầu code này:

```python
import uuid
from pymongo import MongoClient

# Thiết lập chuỗi kết nối cục bộ
client = MongoClient('mongodb://127.0.0.1:27017/')

# Chọn Database (nếu chưa có, MongoDB sẽ tự tạo giúp bạn)
db = client['shop']

# Trỏ đến tập hợp lưu trữ (Collection) có tên là `products`
products_collection = db['products']
```

---

## Bước 4: Chế tạo Bộ điều phối tính năng (CRUD Operations)

Công cụ Generator chỉ làm giúp bạn chiếc "vỏ trống" trả về kết nối mờ mịt `"do some magic!"`. Bạn cần tự viết hoặc thêm logic Create, Read, Update, Delete dùng `PyMongo`. Thay thế các hàm thành nội dung giải thích phía dưới:

*   **Tạo Sản phẩm (Create / POST):**
    ```python
    def create_product(body=None):
       # Lấy dữ liệu gửi từ JSON
       product_input = ProductInput.from_dict(connexion.request.get_json())
       # Dịch sang Model để lưu xuống Mongo (MongoDB nhận dữ liệu dict)
       new_product = {
           "id": str(uuid.uuid4()), # sinh mã ngẫu nhiên cho SP
           "name": product_input.name,
           "description": product_input.description,
           "price": product_input.price
       }
       products_collection.insert_one(new_product)
       return _serialize_product(new_product), 201
    ```

*   **Lấy tất cả sản phẩm (Read / GET):**
    ```python
    def get_products():
       # find({}) -> Có nghĩa là tìm tất cả mà không rào cản bộ lọc nào
       docs = products_collection.find({})
       return [_serialize_product(doc) for doc in docs], 200
    ```

*   **Cập nhật dữ liệu (Update / PUT):** 
    Sẽ dùng `find_one_and_update` đi kèm tuỳ biến `$set` để Database hiểu là "sửa thông tin có sẵn" chứ không cần thiết phải tạo dòng mới.

*   **Xoá đối tượng (Delete / DELETE):**
    ```python
    def delete_product(id):
       result = products_collection.delete_one({"id": id})
       if result.deleted_count == 0:
           return "Product not found", 404
       return "Deleted", 204
    ```

Cuối cùng, gõ lệnh chạy server api này lên:
```bash
python -m openapi_server
```

---

## Bước 5: Kiểm thử API bằng phần mềm Postman

Server đang túc trực sẵn ở Cổng `8080`. Bạn dùng Postman để kiểm tra nó:

1. **Hành động thêm mới SP (Tạo dữ liệu)**
   - Header: `POST`  —  URL: `http://localhost:8080/v1/products`
   - Data Body (chọn dạng Text thành JSON):
     ```json
     { "name": "Bút bi", "price": 1000, "description": "Xanh" }
     ```
   - Nhấn Send và sao chép cái mã `id` siêu dài của nó nha.

2. **Hành động coi kết quả lưu**
   - Header: `GET` — URL: `http://localhost:8080/v1/products`
   - Trả về danh sách nãy giờ!

3. **Hành động Sửa hoặc Xoá từng SP cụ thể**
   - Header: `PUT` (Sửa ráp JSON mới) hoặc `DELETE`
   - URL: `http://localhost:8080/v1/products/{Mã_ID_khi_nãy}`
   - Nhấn yêu cầu Send.

---

## Bước 6: Soi dữ liệu thô trên Database

Hành động test trên Postman sẽ là giả mạo nếu không thực sự xuống Database kiểm tra:

1. Mở app **MongoDB Compass** (hoặc Extensions MongoDB VS Code).
2. Đường Link URI có sẵn: `mongodb://127.0.0.1:27017/` -> Cứ bấm Connect!
3. Vào danh sách thư mục cột trái: Bấm mở **`shop`** -> Sau đó bấm nhấp vô **`products`**.
4. Ở bảng chính giữa, bạn sẽ thấy tường tận những Object JSON vừa test bị nhét vô đây.

Chúc bạn đạt điểm tối đa ở thực hành buồi 7 này!
