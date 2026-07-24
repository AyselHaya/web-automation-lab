# AI Usage Log

## Entry 1 — Generating dummy book data
**What I was doing:** Creating 20-30 dummy book entries for the sandbox site's items.json.
**Tool & approach:** Used Claude, asked it to generate books matching my BookNook theme with id, title, author, genre, price, rating, description fields.
**What it got right / wrong:** Got the structure and field consistency right on the first try (id, title, author, genre, price, rating, description). Kept genres varied and added recurring authors across multiple books for a bit of realism.
**What I learned:** Generating structured dummy data this way is much faster than writing it by hand, and having a consistent tone across entries makes the demo feel more polished.
## Entry 2 — Building the Flask listing site
**What I was doing:** Building the Flask app, listing page, and detail page with search/pagination.
**Tool & approach:** Used Claude to generate the initial app.py and templates, then ran and tested each route myself before moving on.
**What it got right / wrong:** Structure and Jinja templating worked correctly on first try; verified search and pagination logic manually in the browser.
**What I learned:** Testing each piece (listing, search, detail, borrow flow) immediately after building it — rather than writing everything then testing at the end — made it much easier to know exactly what was working.