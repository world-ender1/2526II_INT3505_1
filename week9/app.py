from flask import Flask, request, jsonify, Response
from datetime import datetime

app = Flask(__name__)

# ==============================================================================
# Bước 1: API v1 (Legacy)
# Payload: { "amount": 100, "currency": "USD" }
# Bước 4: Thêm Deprecation Headers vào API v1
# ==============================================================================
@app.route('/api/v1/payments', methods=['POST'])
def process_payment_v1():
    data = request.get_json()
    
    if not data or 'amount' not in data or 'currency' not in data:
        return jsonify({"error": "Invalid payload. 'amount' and 'currency' are required."}), 400
        
    amount = data['amount']
    currency = data['currency']
    
    # Giả lập xử lý thanh toán
    response_data = {
        "status": "success",
        "message": f"Payment of {amount} {currency} processed (v1).",
        "transaction_id": "TXN_v1_12345"
    }
    
    # Bước 4: Tạo response và thêm Deprecation headers
    response = jsonify(response_data)
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Thu, 31 Dec 2026 23:59:59 GMT'
    response.headers['Link'] = '<http://localhost:5000/docs/migration>; rel="deprecation"'
    response.headers['Warning'] = '299 - "API v1 is deprecated and will be removed. Please migrate to v2."'
    
    return response

# ==============================================================================
# Bước 2: API v2 với Breaking Changes (URL Versioning)
# Payload: 
# { 
#   "price": { "amount": 100, "currency": "USD" },
#   "payment_method": "credit_card" 
# }
# ==============================================================================
@app.route('/api/v2/payments', methods=['POST'])
def process_payment_v2():
    data = request.get_json()
    
    if not data or 'price' not in data or 'payment_method' not in data:
        return jsonify({"error": "Invalid payload. 'price' and 'payment_method' are required."}), 400
        
    price = data['price']
    
    if 'amount' not in price or 'currency' not in price:
         return jsonify({"error": "Invalid payload. 'price' must contain 'amount' and 'currency'."}), 400
         
    amount = price['amount']
    currency = price['currency']
    method = data['payment_method']
    
    # Giả lập xử lý thanh toán
    response_data = {
        "status": "success",
        "message": f"Payment of {amount} {currency} via {method} processed (v2).",
        "transaction_id": "TXN_v2_98765"
    }
    
    return jsonify(response_data)

# ==============================================================================
# Bước 3: Triển khai Query Param & Header Versioning
# Route chung: /api/payments
# ==============================================================================
@app.route('/api/payments', methods=['POST'])
def process_payment_general():
    # 1. Kiểm tra Header Versioning trước (Ưu tiên)
    # Ví dụ Header: X-API-Version: 2
    header_version = request.headers.get('X-API-Version')
    if header_version:
        if header_version == '2':
            return process_payment_v2()
        elif header_version == '1':
            return process_payment_v1()
        else:
            return jsonify({"error": "Unsupported API Version in Header"}), 400

    # 2. Kiểm tra Query Param Versioning nếu không có Header
    # Ví dụ Query: ?v=2
    query_version = request.args.get('v')
    if query_version:
        if query_version == '2':
            return process_payment_v2()
        elif query_version == '1':
            return process_payment_v1()
        else:
            return jsonify({"error": "Unsupported API Version in Query Params"}), 400
            
    # Mặc định gọi v1 nếu không chỉ định version (hoặc trả lỗi tùy chiến lược)
    # Ở đây ta chọn fallback về v1 để đảm bảo backward compatibility cho client cũ
    return process_payment_v1()

if __name__ == '__main__':
    print("="*60)
    print("Starting Payment API Server...")
    print("Endpoints:")
    print(" - POST /api/v1/payments (URL Versioning - Deprecated)")
    print(" - POST /api/v2/payments (URL Versioning - Latest)")
    print(" - POST /api/payments?v=1 or ?v=2 (Query Param Versioning)")
    print(" - POST /api/payments with X-API-Version header (Header Versioning)")
    print("="*60)
    app.run(debug=True, port=5000)
