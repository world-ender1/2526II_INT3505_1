# Demo API Testing & Quality Assurance - Tuần 8

Tài liệu này cung cấp mã nguồn và hướng dẫn để thực hiện demo các khái niệm: Unit Testing, Integration Testing, và Performance Testing cho API theo yêu cầu Chương 8 môn SOA.

### 📌 Các Loại Test Được Áp Dụng Trong Bài:
1. **Unit Test (Kiểm thử mức đơn vị):** Được thể hiện qua các lệnh kiểm tra cơ bản trong Postman như `pm.response.to.have.status(200);` (đảm bảo logic của 1 endpoint đơn lẻ trả về đúng mã trạng thái) hay kiểm tra cấu trúc dữ liệu cơ bản.
2. **Integration Test (Kiểm thử tích hợp):** Được thể hiện bằng việc lưu biến môi trường (ví dụ: ID sản phẩm mới tạo ở API POST) và truyền nó vào các API tiếp theo (GET/PUT/DELETE) để kiểm tra luồng dữ liệu liên kết giữa nhiều endpoint và cơ sở dữ liệu.
3. **Performance / Load Test (Kiểm thử hiệu năng):** Được thực hiện ở phần cuối bằng công cụ **Locust**, mô phỏng hàng trăm người dùng ảo gửi request liên tục để đo lường tốc độ phản hồi (Response Time) và tỷ lệ lỗi (Error Rate) khi hệ thống chịu tải.

## Phần 1: Xây dựng API Mẫu (Flask)
Để có hệ thống test, trước tiên ta cần 1 API nhỏ với 5 endpoints cơ bản (CRUD).

Tạo file `app.py`:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database tạm thời
products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Mouse", "price": 50}
]

# 1. GET /products - Lấy danh sách sản phẩm
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

# 2. GET /products/<id> - Lấy chi tiết 1 sản phẩm
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# 3. POST /products - Tạo sản phẩm mới
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_product = {
        "id": len(products) + 1,
        "name": data['name'],
        "price": data['price']
    }
    products.append(new_product)
    return jsonify(new_product), 201

# 4. PUT /products/<id> - Cập nhật sản phẩm
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product['name'] = data.get('name', product['name'])
        product['price'] = data.get('price', product['price'])
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# 5. DELETE /products/<id> - Xóa sản phẩm
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Phần 2: Viết Test trong Postman cho 5 Endpoints

Trong Postman, sau khi thiết lập Request cho mỗi endpoint, bạn chuyển sang tab **Tests** và dán các đoạn mã JavaScript sau để tự động kiểm tra (Assert) kết quả.

### 1. Test Endpoint: `GET /products`
```javascript
// [UNIT TEST] Kiểm tra Status Code cơ bản
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// [PERFORMANCE TEST] Đo Response time
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});

// [INTEGRATION TEST] Kiểm tra cấu trúc dữ liệu trả về từ Database
pm.test("Response is an array of products", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an("array");
    pm.expect(jsonData[0]).to.have.property("id");
    pm.expect(jsonData[0]).to.have.property("name");
});
```

### 2. Test Endpoint: `POST /products`
*Lưu ý: Cần thêm Body JSON: `{"name": "Keyboard", "price": 120}`*
```javascript
// [UNIT TEST] Kiểm tra mã trạng thái tạo thành công
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

// [INTEGRATION TEST] Kiểm tra kết quả tạo mới & Lưu biến dùng chung
pm.test("Product created successfully with correct data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("id");
    pm.expect(jsonData.name).to.eql("Keyboard");
    
    // Lưu ID sản phẩm mới tạo vào biến môi trường để dùng cho request tiếp theo
    pm.environment.set("new_product_id", jsonData.id);
});
```

### 3. Test Endpoint: `GET /products/{{new_product_id}}`
```javascript
// [UNIT TEST] Kiểm tra trạng thái trả về
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// [INTEGRATION TEST] Xác minh xem hệ thống có lấy đúng ID sản phẩm vừa tạo ở bước POST không
pm.test("Check correct product retrieved", function () {
    var jsonData = pm.response.json();
    // Lấy ID từ biến môi trường để so sánh
    var expectedId = parseInt(pm.environment.get("new_product_id"));
    pm.expect(jsonData.id).to.eql(expectedId);
});
```

### 4. Test Endpoint: `PUT /products/{{new_product_id}}`
*Lưu ý: Cần thêm Body JSON: `{"price": 150}`*
```javascript
// [UNIT TEST] Kiểm tra trạng thái cập nhật
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// [INTEGRATION TEST] Kiểm tra xem dữ liệu sau khi PUT có thực sự thay đổi trong Database không
pm.test("Price updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.price).to.eql(150); // Kiểm tra giá đã được update
});
```

### 5. Test Endpoint: `DELETE /products/{{new_product_id}}`
```javascript
// [UNIT TEST] Kiểm tra trạng thái xóa
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// [UNIT TEST] Kiểm tra message phản hồi từ server
pm.test("Delete confirmation message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.eql("Product deleted");
});
```

## Phần 3: Chạy Tự Động Hóa với Newman

**Newman** là công cụ dòng lệnh (CLI) giúp bạn chạy hàng loạt kịch bản test của Postman, rất hữu ích cho CI/CD.

**Các bước thực hiện:**

1. **Cài đặt Newman** (Yêu cầu máy cài sẵn Node.js):
```bash
npm install -g newman
npm install -g newman-reporter-htmlextra  # Gói tạo báo cáo UI đẹp
```

2. **Sử dụng trực tiếp file Collection có sẵn**:
   - Bạn có thể dùng luôn file `postman_collection.json` đã được tạo sẵn trong dự án. File này đã được tích hợp toàn bộ API và biến môi trường `base_url`.

3. **Chạy tự động trên Terminal**:
```bash
# Lệnh chạy cơ bản
newman run postman_collection.json

# Lệnh chạy và xuất báo cáo HTML (Test Report siêu đẹp)
newman run postman_collection.json -r htmlextra
```
*(Báo cáo sẽ được tự động tạo trong thư mục `newman/` với biểu đồ trực quan về số lượng API pass/fail)*


## Phần 4: Đo Hiệu Năng API (Load Testing / Performance Testing)

Thay vì Postman, để đo hiệu năng thực tế với số lượng truy cập lớn (Load Testing), công cụ **Locust** (Python) hoặc **k6** thường được dùng. Dưới đây là demo dùng Locust.

1. **Cài đặt Locust**:
```bash
pip install locust
```

2. **Tạo kịch bản giả lập người dùng `locustfile.py`**:
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    # Thời gian chờ random giữa các request (1 đến 3 giây)
    wait_time = between(1, 3)

    @task(3) # Trọng số 3: Tần suất gọi endpoint này nhiều gấp 3 lần endpoint dưới
    def get_all_products(self):
        # Giả lập thao tác người dùng lấy danh sách sản phẩm
        self.client.get("/products", name="GET /products")

    @task(1)
    def get_single_product(self):
        self.client.get("/products/1", name="GET /products/[id]")

    @task(1)
    def create_product(self):
        self.client.post("/products", json={"name": "Load Test Item", "price": 99}, name="POST /products")
```

3. **Chạy và Theo Dõi Hiệu Năng**:
```bash
locust -f locustfile.py
```
- Mở trình duyệt và truy cập Web UI của Locust: `http://localhost:8089`
- Nhập thông số demo:
  - **Number of users**: 500 (Số lượng người dùng đồng thời)
  - **Spawn rate**: 10 (Thêm 10 người dùng mỗi giây)
  - **Host**: `http://localhost:5000` (URL của server API Flask)
- Bấm **Start swarming**.
- Bạn sẽ có thể demo trực quan cho thầy cô các thông số hiệu năng:
  - **Response Time (ms)**: Tốc độ phản hồi trung bình/Max/Min
  - **RPS (Requests Per Second)**: Số request xử lý trong 1 giây
  - **Error Rate (%)**: Tỷ lệ lỗi khi server bị quá tải.
