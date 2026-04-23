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
