# Project Planning — BookNook (Sandbox Listing Site)

## Theme
A local sandbox bookstore listing site: browse and search books by title, author, or genre.

## Data Model (items.json)
Each book has:
- id
- title
- author
- genre (e.g. Fiction, Sci-Fi, Mystery, Romance, Non-fiction)
- price
- rating (1-5)
- description (1-2 sentences)

20-40 dummy books, generated with AI.

## Site Pages
- **Listing page**: shows all books, paginated ("load more" button), with a search/filter box (by title, author, or genre)
- **Detail page**: full info per book, with a "Request to Borrow" button that opens a small dummy form (name + confirm) to submit

## Bot Workflow
1. Open the listing page
2. Search/filter for a target keyword (e.g. a genre or author name)
3. Open the top 3 matching results' detail pages
4. On each: click "Request to Borrow," fill and submit the dummy form
5. Extract confirmation + book details, log the outcome
6. Produce a run summary: books processed, disruptions hit, how each was resolved

## Chaos Engine Scenarios (Core 8 — all required)
1. Random popup/modal (newsletter signup)
2. Cookie/consent banner
3. Simulated captcha gate (before the borrow form submits)
4. Site down/server errors (500/503 on search or detail pages)
5. Slow responses/timeouts (random delay on search results)
6. Unexpected redirection (search sometimes lands on a promo page)
7. DOM change/selector drift (alternate layout for listing/detail pages)
8. Blocked/intercepted clicks (sticky banner over the "Request to Borrow" button)

## Stretch Scenarios (after core 8 work)
- Rate-limit (429) responses on repeated searches
- Session/state expiry mid-run
- **Original scenario 1 — "The Wrong Book":** detail page occasionally loads showing a different book than the one searched (simulated stale-link bug). Bot must verify the displayed title matches the search target before trusting/extracting data.
- **Original scenario 2 — "Sold Out Mid-Checkout":** a book shows available on the listing page but is randomly unavailable when the bot attempts "Request to Borrow" (simulated race condition). Bot must recognize this as a valid outcome (not an error), log it, and move to the next result rather than retrying indefinitely.


## Tech Stack
- Flask (Python) serving simple HTML templates, no DB
- Playwright (Python, sync API) for the bot
- pytest for testing

## Risks / Open Questions
- Need to decide exact handling strategy per scenario (will refine as I build)
- Selector strategy: keep all selectors centralized in `bot/selectors.py` with fallback chains from the start, so DOM-change scenario doesn't require a rewrite later
