import sys
import os

sys.path.append(os.path.dirname(__file__))

from playwright.sync_api import sync_playwright
import selectors as sel
from reporting import new_run_log, log_event, save_screenshot, finish_run

BASE_URL = "http://127.0.0.1:5000"
SEARCH_TERM = "Fiction"


def run_bot():
    run_log = new_run_log()
    log_event(run_log, "Starting bot run")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            log_event(run_log, f"Navigating to {BASE_URL}")
            page.goto(BASE_URL)

            log_event(run_log, f"Searching for '{SEARCH_TERM}'")
            page.fill(sel.SEARCH_INPUT, SEARCH_TERM)
            page.click(sel.SEARCH_SUBMIT)
            page.wait_for_load_state("networkidle")

            book_links = page.locator(sel.BOOK_LINKS)
            count = book_links.count()
            log_event(run_log, f"Found {count} search results")

            top_n = min(3, count)
            for i in range(top_n):
                title = book_links.nth(i).inner_text()
                log_event(run_log, f"Opening result {i+1}: {title}")
                book_links.nth(i).click()
                page.wait_for_load_state("networkidle")

                log_event(run_log, "Clicking Request to Borrow")
                page.click(sel.BORROW_BUTTON)
                page.fill(sel.BORROWER_NAME_INPUT, "BookBot")
                page.click(sel.CONFIRM_BORROW_BUTTON)

                confirmation = page.locator(sel.CONFIRMATION_TEXT).inner_text()
                log_event(run_log, f"Confirmation received: {confirmation}")
                run_log["items_processed"] += 1

                save_screenshot(page, run_log, f"item_{i+1}_done")

                page.go_back()
                page.wait_for_load_state("networkidle")
                page.go_back()
                page.wait_for_load_state("networkidle")
                page.fill(sel.SEARCH_INPUT, SEARCH_TERM)
                page.click(sel.SEARCH_SUBMIT)
                page.wait_for_load_state("networkidle")
                book_links = page.locator(sel.BOOK_LINKS)

        except Exception as e:
            log_event(run_log, f"ERROR: {str(e)}")
            save_screenshot(page, run_log, "error_state")

        finally:
            browser.close()
            finish_run(run_log)


if __name__ == "__main__":
    run_bot()