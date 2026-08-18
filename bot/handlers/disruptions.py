import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import bot_selectors as sel


def dismiss_popup_if_present(page, run_log, log_event):
    popup = page.locator(sel.POPUP_CONTAINER)
    if popup.count() > 0 and popup.is_visible():
        log_event(run_log, "Detected popup — dismissing")
        run_log["disruptions_encountered"] += 1
        page.locator(sel.POPUP_DISMISS_BUTTON).click()
        popup.wait_for(state="hidden", timeout=3000)
        log_event(run_log, "Popup dismissed")


def accept_cookies_if_present(page, run_log, log_event):
    banner = page.locator(sel.COOKIE_BANNER)
    if banner.count() > 0 and banner.is_visible():
        log_event(run_log, "Detected cookie banner — accepting")
        run_log["disruptions_encountered"] += 1
        page.locator(sel.COOKIE_ACCEPT_BUTTON).click()
        banner.wait_for(state="hidden", timeout=3000)
        log_event(run_log, "Cookie banner accepted")


def dismiss_overlay_if_present(page, run_log, log_event):
    overlay = page.locator(sel.BLOCKED_OVERLAY)
    if overlay.count() > 0 and overlay.is_visible():
        log_event(run_log, "Detected blocking overlay on borrow button — dismissing")
        run_log["disruptions_encountered"] += 1
        page.locator(sel.BLOCKED_OVERLAY_DISMISS).click()
        overlay.wait_for(state="hidden", timeout=3000)
        log_event(run_log, "Overlay dismissed")


def handle_known_disruptions(page, run_log, log_event):
    """Checks for listing-page-level disruptions (popup, cookie banner)."""
    dismiss_popup_if_present(page, run_log, log_event)
    accept_cookies_if_present(page, run_log, log_event)


def solve_captcha_if_present(page, run_log, log_event, max_attempts=3):
    hidden_answer = page.locator(sel.CAPTCHA_HIDDEN_ANSWER)
    if hidden_answer.count() == 0:
        return False
    log_event(run_log, "Detected captcha gate — solving")
    run_log["disruptions_encountered"] += 1
    answer_value = hidden_answer.get_attribute("value")
    page.fill(sel.CAPTCHA_ANSWER_INPUT, answer_value)
    page.click(sel.CAPTCHA_SUBMIT_BUTTON)
    page.wait_for_load_state("networkidle")
    log_event(run_log, "Captcha solved, proceeding")
    return True