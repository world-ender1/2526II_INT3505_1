from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# --- GIẢ LẬP DATABASE ---
books_db = [
    {"id": i, "title": f"Lập trình Python Tập {i}", "author": "James Higginbotham", "category": "Technical"}
    for i in range(1, 51)
]

loans_db = [
    {"id": 101, "member_id": "M001", "book_id": 1, "status": "borrowed"},
    {"id": 102, "member_id": "M001", "book_id": 5, "status": "returned"},
]

# --- ENDPOINTS ---

# 1. Resource: /books (Danh sách sách với Phân trang Offset-based)
# Thử truy cập: http://127.0.0.1:5000/books?page=2&limit=5
@app.route('/books', methods=['GET'])
def get_books():
    # Lấy tham số từ query string, mặc định page=1 và limit=10
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    if page < 1 or limit < 1:
        abort(400, description="Page và Limit phải lớn hơn 0")

    start = (page - 1) * limit
    end = start + limit
    
    results = books_db[start:end]
    
    return jsonify({
        "metadata": {
            "total_records": len(books_db),
            "current_page": page,
            "limit": limit,
            "has_next": end < len(books_db)
        },
        "data": results
    })

# 2. Resource Tree: /members/<id>/loans (Sub-resource)
# Thử truy cập: http://127.0.0.1:5000/members/M001/loans
@app.route('/members/<string:member_id>/loans', methods=['GET'])
def get_member_loans(member_id):
    # Lọc dữ liệu mượn sách của thành viên cụ thể
    member_loans = [loan for loan in loans_db if loan["member_id"] == member_id]
    
    if not member_loans:
        return jsonify({"error": "Không tìm thấy dữ liệu cho thành viên này"}), 404

    return jsonify({
        "resource_path": f"/members/{member_id}/loans",
        "member_id": member_id,
        "loans": member_loans
    })

# 3. Tìm kiếm (Search)
# Thử truy cập: http://127.0.0.1:5000/books/search?q=Python
@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Vui lòng nhập từ khóa tìm kiếm"}), 400

    filtered = [b for b in books_db if query.lower() in b['title'].lower()]
    
    return jsonify({
        "query": query,
        "count": len(filtered),
        "results": filtered
    })

if __name__ == '__main__':
    app.run(debug=True)