import sys
import os
from flask import jsonify, request, abort
import connexion
from dotenv import load_dotenv

# Thêm thư mục gốc vào sys.path để connexion có thể import api.index
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load biến môi trường từ .env
load_dotenv()

# In-memory data store
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999},
]
next_id = 3


def get_all_books():
    """Lấy danh sách tất cả sách"""
    return books, 200


def get_book_by_id(book_id):
    """Lấy sách theo ID"""
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description=f"Book with id {book_id} not found")
    return book, 200


def create_book():
    """Tạo sách mới"""
    global next_id
    if connexion.request.is_json:
        data = connexion.request.get_json()
    else:
        abort(400, description="Request body must be JSON")

    new_book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year"),
    }
    books.append(new_book)
    next_id += 1
    return new_book, 201


# Khởi tạo Connexion App
app = connexion.FlaskApp(__name__, specification_dir='../')

# Đọc file openapi.yaml và thiết lập Swagger UI tại /ui
app.add_api('openapi.yaml', arguments={'title': 'Book Management API'})

# Lấy ra underlying Flask app object để Vercel sử dụng
application = app.app

# Thêm route root
@application.route("/", methods=["GET"])
def index():
    server_url = os.getenv("SERVER_URL", "https://your-project.vercel.app")
    return jsonify({
        "message": "Welcome to Book API",
        "docs": f"{server_url}/ui",
        "openapi_spec": f"{server_url}/openapi.json"
    }), 200


if __name__ == "__main__":
    app.run(port=8080, debug=True)
