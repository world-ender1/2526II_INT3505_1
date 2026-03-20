from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory data store
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999},
]
next_id = 3


@app.route("/books", methods=["GET"])
def get_all_books():
    """Lấy danh sách tất cả sách"""
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    """Lấy sách theo ID"""
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description=f"Book with id {book_id} not found")
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    """Tạo sách mới"""
    global next_id
    data = request.get_json()

    if not data:
        abort(400, description="Request body must be JSON")

    for field in ["title", "author"]:
        if field not in data:
            abort(400, description=f"Missing required field: '{field}'")

    new_book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year"),
    }
    books.append(new_book)
    next_id += 1
    return jsonify(new_book), 201


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400


if __name__ == "__main__":
    app.run(port=8080, debug=True)
