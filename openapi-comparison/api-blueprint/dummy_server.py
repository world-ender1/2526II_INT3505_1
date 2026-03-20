from flask import Flask, jsonify, request

app = Flask(__name__)

books = [{
    "id": 101,
    "title": "The Lord of the Rings",
    "author": "J.R.R. Tolkien",
    "publishedYear": 1954
}]

@app.route("/v1/books", methods=["GET"])
def get_books():
    return jsonify(books), 200

@app.route("/v1/books", methods=["POST"])
def add_book():
    data = request.json
    new_book = {
        "id": 102,
        "title": data.get("title"),
        "author": data.get("author"),
        "publishedYear": data.get("publishedYear")
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if book_id == 101:
        return jsonify(books[0]), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)
