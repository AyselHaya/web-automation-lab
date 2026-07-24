from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load book data once at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "items.json")

def load_books():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def listing():
    books = load_books()

    # Basic search/filter by title, author, or genre
    query = request.args.get("q", "").strip().lower()
    if query:
        books = [
            b for b in books
            if query in b["title"].lower()
            or query in b["author"].lower()
            or query in b["genre"].lower()
        ]

    # Simple "load more" pagination
    page_size = 10
    page = int(request.args.get("page", 1))
    total_pages = max(1, (len(books) + page_size - 1) // page_size)
    start = (page - 1) * page_size
    end = start + page_size
    books_page = books[start:end]

    return render_template(
        "listing.html",
        books=books_page,
        query=query,
        page=page,
        total_pages=total_pages
    )

@app.route("/book/<int:book_id>")
def detail(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return "Book not found", 404
    return render_template("detail.html", book=book)

if __name__ == "__main__":
    app.run(debug=True, port=5000)