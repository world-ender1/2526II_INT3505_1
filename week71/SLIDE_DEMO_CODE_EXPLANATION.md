# Ánh Xạ Giữa Slide 4 Bước Trình Bày Và Source Code Demo

Tài liệu này là kịch bản (script) để bạn trình bày, kết hợp giữa 4 bước trên slide và những thao tác chi tiết được trích ra từ file hướng dẫn demo để bạn dễ dàng biểu diễn trên máy.

---

## Bước 1: Viết Contract (OpenAPI Spec)

**Mục tiêu trong Slide:** Xác định các Paths, Methods, Parameters, Request Body, mã phản hồi (Response Codes) và tối ưu với Components.  
**File Demo:** `api.yaml`

**Giải thích & Code trực quan khi trình bày:**
File `api.yaml` là bản thiết kế hợp đồng API chuẩn. Bạn hày mở file này lên và đối chiếu trực tiếp từng đoạn code với các từ khóa nằm trên slide của bạn:

**1. Paths & Methods (Đường dẫn & Phương thức):**
Khai báo cụ thể các endpoint thiết yếu là `/products` và khoảng route mang ID là `/products/{id}`. Dưới các Path này, gắn các Method như `get`, `post`, `put`, `delete`.
```yaml
paths:
  /products:
    get:
      summary: Get all products
    post:
      summary: Create a product
  
  /products/{id}:
    get:
      summary: Get a product by ID
    put:
      summary: Update a product
    delete:
      summary: Delete a product
```

**2. Parameters (Định nghĩa tham số cho API):**
Đối với đường dẫn `/products/{id}`, ta phải định nghĩa rõ tham số `id` là gì, nằm ở đâu (`in: path` hay query hay header).
```yaml
  /products/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
```

**3. Request Body (Thân của yêu cầu - dùng cho POST/PUT):**
Đảm bảo Client gửi dữ liệu đúng định dạng JSON, có cấu trúc chặt chẽ.
```yaml
    post:
      summary: Create a product
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProductInput' # Chỉ tay về thư viện Component
```

**4. Mã phản hồi (Response Codes cho Frontend):**
Định nghĩa rõ ràng các mã lỗi để hệ thống rành mạch rỏ ràng. `201` là tạo thành công, `204` là xóa xong (no content), `404` là không tìm thấy.
```yaml
      responses:
        '201': # <-- Mã phản hồi tạo thành công
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404': # <-- Báo lỗi
          description: Product not found
```

**5. Tối ưu với Components:**
Slide có ghi "Tối ưu hóa với Components", đây là phần mấu chốt. Thay vì copy-paste khuôn cấu trúc dài thòng lọng ở mọi nơi, ta gói thành một "Schema" đặt ở cuối cấu trúc và chỉ cần chỉ `$ref` tới đó.
```yaml
components:
  schemas:
    Product:
      type: object
      required:
        - id
        - name
        - price
      properties:
        id:
          type: string
        name:
          type: string # ... các thuộc tính khác
    ProductInput: # Dành riêng cho dữ liệu đầu vào (tạo mới không truyền id)
      type: object
      required:
        - name
        - price
```

---

## Bước 2: Sinh Code Tự Động

**Mục tiêu trong Slide:** Chạy lệnh Codegen đê tự động sinh ra cấu trúc routes, controllers, cài đặt dependencies.

**Thao tác Demo thực tế (Trích từ Tutorial):**
1. **Sinh code:** Mở terminal, chứng minh sức mạnh của OpenAPI-Generator bằng cách gõ lệnh duy nhất này để biến `api.yaml` thành code thật:
   ```bash
   npx @openapitools/openapi-generator-cli generate -i api.yaml -g python-flask -o .
   ```
   *Lệnh này sinh ra thư mục cấu trúc bộ não Backend là `openapi_server` và danh sách thư viện `requirements.txt`*

2. **Khởi tạo môi trường ảo & cấu hình dependencies:**
   Để máy chủ gọn gàng, không bị xung đột, bạn tiếp tục demo việc cấu hình Python:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt pymongo
   ```

---

## Bước 3: Cài đặt & Kết nối Database (Sức mạnh của PyMongo)

**Mục tiêu trong Slide:** Lấy Connection string, thiết lập biến môi trường và viết code kết nối với MongoDB.  
**File Demo:** `openapi_server/controllers/default_controller.py`

**Giải thích & Code khi trình bày:**
Mở đoạn đầu file `default_controller.py`, giải thích cách kết nối an toàn với MongoDB thông qua thư viện `pymongo`. 

> **Nói thêm về PyMongo:** PyMongo là trình điều khiển (Driver) chính thức của ngôn ngữ Python để giao tiếp với Cơ sở dữ liệu NoSQL MongoDB. Thay vì phải viết các câu lệnh truy vấn cấu trúc phức tạp, PyMongo giúp chúng ta thao tác với Database như đang thao tác với các List và Dictionary (Object) thông thường bên trong Python.

```python
import uuid
from pymongo import MongoClient

# 1. MongoClient: Tạo một "Đường ống" kết nối duy trì liên tục đến CSDL đang chạy.
# Ở đây ta dùng chuỗi kết nối cục bộ (Hoặc URI MongoDB Atlas nếu xài Cloud)
client = MongoClient('mongodb://127.0.0.1:27017/')

# 2. Truy cập Database: Cách thức linh hoạt của PyMongo là khi gọi client['shop'], 
# nếu DB 'shop' chưa tồn tại, MongoDB sẽ ngầm hiểu và tự động tạo mới giúp bạn.
db = client['shop']

# 3. Truy cập Collection: Tương tự như DB, nó trỏ tới tập hợp 'products' 
# (giống như "Table" trong SQL) để chuẩn bị nhúng dữ liệu.
products_collection = db['products']
```

---

## Bước 4: Hoàn Thiện Cài Đặt Service (Thực thi Logic CRUD bằng thư viện PyMongo)

**Mục tiêu trong Slide:** Import Data Model và viết các code logic trực tiếp cho các hành động Create, Read, Update, Delete.

**Giải thích khi trình bày (Trích từ Tutorial):**
Lệnh Sinh code (Bước 2) chỉ tạo ra "phần khung" tiếp nhận tín hiệu từ Frontend. Phần "Lõi" (thao tác lưu/sửa với Database) sẽ do lập trình viên khai thác các cú pháp tuyệt vời của **PyMongo** ở file `default_controller.py`.

**0. Nạp Data Model & Chuẩn bị Hàm Hỗ Trợ (Import Data Model):**
Mở đầu khu vực thay đổi logic (vẫn trong file `default_controller.py`), chúng ta phải nạp các Model vào để làm "khuôn ép kiểu" nhằm đảm bảo tính toàn vẹn của dữ liệu Backend.

```python
# Nạp Data Model (Khuôn chuẩn Product và ProductInput do Codegen tự dựng sẵn)
from openapi_server.models.product import Product
from openapi_server.models.product_input import ProductInput

# Viết một helper function nhỏ để dập khuôn dữ liệu thô bị méo mó của database thành Object Product đẹp mắt
def _serialize_product(doc):
    return Product(
        id=doc.get("id"),
        name=doc.get("name"),
        description=doc.get("description"),
        price=doc.get("price")
    )
```

**1. Hành động Tạo Mới (POST - Create):**
```python
def create_product(body=None):
    product_input = ProductInput.from_dict(connexion.request.get_json()) 
    new_product = {
        "id": str(uuid.uuid4()), # Khởi tạo ID rỗng
        "name": product_input.name,
        "description": product_input.description,
        "price": product_input.price
    }
    # [PYMONGO API]: Hàm insert_one()
    # Nhận vào một Dictionary Python và ném trực tiếp thành 1 Document (hàng) lưu xuống MongoDB.
    products_collection.insert_one(new_product) 
    
    return _serialize_product(new_product), 201
```

**2. Hành động Lọc Danh Sách (GET - Read):**
```python
def get_products():
    # [PYMONGO API]: Hàm find()
    # Nếu truyền JSON rỗng {}, nó sẽ quét sạch bảng. 
    # Lưu ý: method này trả về 1 'Cursor' (Con trỏ) giúp tối ưu RAM, ta dùng vòng lặp (List Comprehension) để nhét nó thành List hoàn chỉnh trả về cho Frontend.
    docs = products_collection.find({}) 
    return [_serialize_product(doc) for doc in docs], 200
```

**3. Hành động Cập Nhật (PUT - Update):**
```python
def update_product(id, body=None):
    # ... Lược bỏ đoạn gán map dữ liệu json update_data cho ngắn ...
    
    from pymongo import ReturnDocument
    
    # [PYMONGO API]: Hàm find_one_and_update()
    # Đây là thao tác Cập nhật Nguyên tử (Atomic). 
    # - Bộ lọc thứ nhất {"id": id}: Tìm đúng mục tiêu.
    # - Bộ lọc thứ hai {"$set": update_data}: Lệnh cực kì then chốt của Mongo, ép kiểu "Chỉ cập nhật những fields nằm trong update_data, giữ nguyên phần còn lại".
    # - return_document=AFTER: Trả về phiên bản Đã Sửa Mới Nhất để show lại cho Front-End.
    doc = products_collection.find_one_and_update( 
        {"id": id},
        {"$set": update_data}, 
        return_document=ReturnDocument.AFTER
    )
    return _serialize_product(doc), 200
```

**4. Hành động Xóa (DELETE - Delete):**
```python
def delete_product(id):
    # [PYMONGO API]: Hàm delete_one()
    # Xoá chuẩn xác 1 đối tượng. Đối tượng result trả về sở hữu thuộc tính `deleted_count`.
    result = products_collection.delete_one({"id": id})
    
    if result.deleted_count == 0: # Check nếu không tìm thấy để xoá
        return "Product not found", 404
        
    return "Deleted", 204
```

Sau khi hoàn tất giải thích hàm, bắt đầu chạy Server lên phục vụ Demo:
```bash
python -m openapi_server
```

---

## 🌟 Bước Bổ sung (Demo Chứng minh Kết Quả) 🌟

*Để buổi thuyết trình thuyết phục, bạn cần thao tác test thực tế dựa trên Server vừa chạy.*

**1. Gửi lệnh giả lập ở Postman**
* Server hiển thị tại URL `http://localhost:8080/v1`.
* Hành động: Mở Postman gửi lệnh `POST http://localhost:8080/v1/products` với Body RAW JSON dạng: `{ "name": "Bút bi", "price": 1000, "description": "Màu Xanh" }` 
* Trả về kết quả Thành công (Mã 201), sao chép mã `id`.
* Thực hiện gửi thử lệnh `GET` để xem kho hàng đã có sản phẩm đó chưa.

**2. Soi Dữ Liệu Thực trong MongoDB Compass:** 
* Mở **MongoDB Compass**.
* Vào địa chỉ `mongodb://127.0.0.1:27017/`.
* Chọn Database **`shop`** -> Truy cập cụm **`products`**.
* Trình diễn rằng Object JSON vừa POST ở Postman, sau khi lọt qua Backend đã an tọạ thật sự dưới phần cứng cơ sở dữ liệu như thế nào. Chốt lại vấn đề.
