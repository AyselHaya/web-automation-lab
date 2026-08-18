import sys
import os

sys.path.append(os.path.dirname(__file__))

from playwright.sync_api import sync_playwright
import selectors as sel
from reporting import new_run_log, log_event, save_screenshot, finish_run
from handlers.disruptions import handle_known_disruptions, solve_captcha_if_present
from handlers.resilience import with_retry
from handlers.navigation import ensure_reached_detail_page

BASE_URL = "http://127.0.0.1:5000"
SEARCH_TERM = "Fiction"


def run_bot():
    run_log = new_run_log()
    log_event(run_log, "Starting bot run")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            ok = with_retry(lambda: page.goto(BASE_URL), page, run_log, log_event, "loading listing page")
            if not ok:
                raise Exception("Could not load listing page after retries")
            handle_known_disruptions(page, run_log, log_event)

            log_event(run_log, f"Searching for '{SEARCH_TERM}'")
            page.fill(sel.SEARCH_INPUT, SEARCH_TERM)
            ok = with_retry(lambda: page.click(sel.SEARCH_SUBMIT), page, run_log, log_event, "searching")
            if not ok:
                raise Exception("Search failed after retries")
            handle_known_disruptions(page, run_log, log_event)

            book_links = page.locator(sel.BOOK_LINKS)
            count = book_links.count()
            log_event(run_log, f"Found {count} search results")

            top_n = min(3, count)
            for i in range(top_n):
                title = book_links.nth(i).inner_text()
                log_event(run_log, f"Opening result {i+1}: {title}")

                ok = with_retry(lambda: book_links.nth(i).click(), page, run_log, log_event, f"opening {title}")
                if not ok:
                    log_event(run_log, f"Skipping {title} — could not load after retries")
                    continue

                reached = ensure_reached_detail_page(page, run_log, log_event, solve_captcha_if_present)
                if not reached:
                    log_event(run_log, f"Could not reach detail page for {title} — skipping")
                    continue

                log_event(run_log, "Clicking Request to Borrow")
                page.click(sel.BORROW_BUTTON)
                page.fill(sel.BORROWER_NAME_INPUT, "BookBot")
                page.click(sel.CONFIRM_BORROW_BUTTON)

                confirmation = page.locator(sel.CONFIRMATION_TEXT).inner_text()
                log_event(run_log, f"Confirmation received: {confirmation}")
                run_log["items_processed"] += 1

                save_screenshot(page, run_log, f"item_{i+1}_done")

                # Navigate straight back to the listing + search, rather than
                # relying on browser history (which now includes extra
                # captcha/promo detour pages of unpredictable length).
                ok = with_retry(lambda: page.goto(BASE_URL), page, run_log, log_event, "returning to listing")
                if not ok:
                    log_event(run_log, "Could not return to listing — stopping loop")
                    break
                handle_known_disruptions(page, run_log, log_event)
                page.fill(sel.SEARCH_INPUT, SEARCH_TERM)
                ok = with_retry(lambda: page.click(sel.SEARCH_SUBMIT), page, run_log, log_event, "re-searching")
                handle_known_disruptions(page, run_log, log_event)
                book_links = page.locator(sel.BOOK_LINKS)

        except Exception as e:
            log_event(run_log, f"ERROR: {str(e)}")
            save_screenshot(page, run_log, "error_state")

        finally:
            browser.close()
            finish_run(run_log)


if __name__ == "__main__":
    run_bot()