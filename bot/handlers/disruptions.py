import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import selectors as sel


def dismiss_popup_if_present(page, run_log, log_event):
    """Detects and dismisses the newsletter/reminder popup if it's showing."""
    popup = page.locator(sel.POPUP_CONTAINER)
    if popup.count() > 0 and popup.is_visible():
        log_event(run_log, "Detected popup — dismissing")
        run_log["disruptions_encountered"] += 1
        page.click(sel.POPUP_DISMISS_BUTTON)
        popup.wait_for(state="hidden", timeout=3000)
        log_event(run_log, "Popup dismissed")


def accept_cookies_if_present(page, run_log, log_event):
    """Detects and accepts the cookie/consent banner if it's showing."""
    banner = page.locator(sel.COOKIE_BANNER)
    if banner.count() > 0 and banner.is_visible():
        log_event(run_log, "Detected cookie banner — accepting")
        run_log["disruptions_encountered"] += 1
        page.click(sel.COOKIE_ACCEPT_BUTTON)
        banner.wait_for(state="hidden", timeout=3000)
        log_event(run_log, "Cookie banner accepted")


def handle_known_disruptions(page, run_log, log_event):
    """Runs all currently-supported disruption checks, in order."""
    dismiss_popup_if_present(page, run_log, log_event)
    accept_cookies_if_present(page, run_log, log_event)