import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bot"))
sys.path.append(os.path.dirname(__file__))

from playwright.sync_api import sync_playwright
import bot_selectors as sel
from reporting import new_run_log, log_event
from handlers.disruptions import handle_known_disruptions, solve_captcha_if_present, dismiss_overlay_if_present
from handlers.resilience import with_retry
from handlers.navigation import ensure_reached_detail_page
from conftest import set_chaos_config

BASE_URL = "http://127.0.0.1:5000"


def run_single_item_workflow():
    """
    A simplified single-item version of the bot's workflow, used to test
    that one item can be fully processed under a given chaos scenario.
    Returns True if it succeeded, False otherwise.
    """
    run_log = new_run_log()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            ok = with_retry(lambda: page.goto(BASE_URL), page, run_log, log_event, "loading listing page")
            if not ok:
                return False
            handle_known_disruptions(page, run_log, log_event)

            page.fill(sel.SEARCH_INPUT, "Fiction")
            ok = with_retry(lambda: page.locator(sel.SEARCH_SUBMIT).click(), page, run_log, log_event, "searching")
            if not ok:
                return False
            handle_known_disruptions(page, run_log, log_event)

            book_links = page.locator(sel.BOOK_LINKS)
            if book_links.count() == 0:
                return False

            ok = with_retry(lambda: book_links.first.click(), page, run_log, log_event, "opening first result")
            if not ok:
                return False

            reached = ensure_reached_detail_page(page, run_log, log_event, solve_captcha_if_present)
            if not reached:
                return False

            dismiss_overlay_if_present(page, run_log, log_event)
            page.click(sel.BORROW_BUTTON)
            page.fill(sel.BORROWER_NAME_INPUT, "TestBot")
            page.click(sel.CONFIRM_BORROW_BUTTON)

            confirmation = page.locator(sel.CONFIRMATION_TEXT).inner_text()
            return "Thanks" in confirmation
        finally:
            browser.close()


def test_workflow_with_popup_scenario():
    set_chaos_config(["popup"])
    assert run_single_item_workflow() is True


def test_workflow_with_cookie_banner_scenario():
    set_chaos_config(["cookie_banner"])
    assert run_single_item_workflow() is True


def test_workflow_with_captcha_scenario():
    set_chaos_config(["captcha_gate"])
    assert run_single_item_workflow() is True


def test_workflow_with_server_error_scenario():
    set_chaos_config(["server_error"])
    assert run_single_item_workflow() is True


def test_workflow_with_redirect_scenario():
    set_chaos_config(["redirect"])
    assert run_single_item_workflow() is True


def test_workflow_with_dom_drift_scenario():
    set_chaos_config(["dom_drift"])
    assert run_single_item_workflow() is True


def test_workflow_with_blocked_click_scenario():
    set_chaos_config(["blocked_click"])
    assert run_single_item_workflow() is True


def test_chaos_gauntlet_all_scenarios():
    """The full gauntlet: every scenario enabled at once, fixed seed, must still succeed."""
    set_chaos_config(["popup", "cookie_banner", "captcha_gate", "server_error",
                       "slow_response", "redirect", "dom_drift", "blocked_click"])
    assert run_single_item_workflow() is True