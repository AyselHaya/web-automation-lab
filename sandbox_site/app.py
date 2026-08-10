from flask import Flask, render_template, request, redirect
import json
import os
import time
import random as rnd

app = Flask(__name__)

CHAOS_PATH = os.path.join(os.path.dirname(__file__), "chaos.json")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "items.json")

RIDDLES = [
    {"question": "I have pages but I'm not a website. What am I?", "answer": "book"},
    {"question": "What do you call a person who loves reading?", "answer": "reader"},
    {"question": "What's 7 + 5?", "answer": "12"},
]


def load_chaos_config():
    with open(CHAOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def scenario_active(scenario_name):
    config = load_chaos_config()
    scenario = config["scenarios"].get(scenario_name, {})
    if not scenario.get("enabled", False):
        return False
    return rnd.random() < scenario.get("probability", 1.0)


def maybe_fail():
    """Randomly returns True if the server_error scenario should trigger."""
    return scenario_active("server_error")


def maybe_delay():
    """Randomly sleeps for a random duration if the slow_response scenario triggers."""
    config = load_chaos_config()
    scenario = config["scenarios"].get("slow_response", {})
    if not scenario.get("enabled", False):
        return
    if rnd.random() < scenario.get("probability", 0):
        delay = rnd.uniform(
            scenario.get("min_delay_seconds", 2),
            scenario.get("max_delay_seconds", 5)
        )
        time.sleep(delay)


def load_books():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def listing():
    maybe_delay()
    if maybe_fail():
        return "Internal Server Error (simulated)", 503

    books = load_books()

    query = request.args.get("q", "").strip().lower()
    if query:
        books = [
            b for b in books
            if query in b["title"].lower()
            or query in b["author"].lower()
            or query in b["genre"].lower()
        ]

    page_size = 10
    page = int(request.args.get("page", 1))
    total_pages = max(1, (len(books) + page_size - 1) // page_size)
    start = (page - 1) * page_size
    end = start + page_size
    books_page = books[start:end]

    show_popup = scenario_active("popup")
    show_cookie_banner = scenario_active("cookie_banner")
    popup_book_title = rnd.choice(books)["title"] if books else "a hidden gem"

    template_name = "listing_alt.html" if scenario_active("dom_drift") else "listing.html"

    return render_template(
        template_name,
        books=books_page,
        query=query,
        page=page,
        total_pages=total_pages,
        show_popup=show_popup,
        show_cookie_banner=show_cookie_banner,
        popup_book_title=popup_book_title
    )


@app.route("/book/<int:book_id>")
def detail(book_id):
    maybe_delay()
    if maybe_fail():
        return "Internal Server Error (simulated)", 503

    if scenario_active("redirect") and not request.args.get("skip_redirect"):
        return render_template(
            "promo.html",
            original_url=f"/book/{book_id}?skip_redirect=true"
        )

    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return "Book not found", 404

    if scenario_active("captcha_gate") and not request.args.get("verified"):
        riddle = rnd.choice(RIDDLES)
        return render_template(
            "captcha.html",
            riddle=riddle["question"],
            correct_answer=riddle["answer"],
            book_id=book_id
        )

    return render_template("detail.html", book=book)


@app.route("/verify-reader", methods=["POST"])
def verify_reader():
    book_id = int(request.form.get("book_id"))
    answer = request.form.get("answer", "").strip().lower()
    correct_answer = request.form.get("correct_answer", "").strip().lower()

    if answer == correct_answer:
        return redirect(f"/book/{book_id}?verified=true")
    else:
        riddle = rnd.choice(RIDDLES)
        return render_template(
            "captcha.html",
            riddle=riddle["question"],
            correct_answer=riddle["answer"],
            book_id=book_id,
            error="Not quite — try again."
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)