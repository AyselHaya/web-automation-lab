import time

MAX_RETRIES = 5


def is_error_page(page):
    try:
        return "Internal Server Error" in page.content()
    except Exception:
        return False


def with_retry(action, page, run_log, log_event, description):
    """
    Runs `action()` once, then checks for the simulated server error.
    If found, reloads with exponential backoff up to MAX_RETRIES times.
    Returns True if the page eventually loaded successfully, False if it never did.
    """
    action()
    page.wait_for_load_state("networkidle")

    attempt = 0
    while is_error_page(page) and attempt < MAX_RETRIES:
        attempt += 1
        run_log["retries"] += 1
        run_log["disruptions_encountered"] += 1
        wait_time = min(2 ** attempt, 10)
        log_event(run_log, f"Server error during '{description}' — retrying in {wait_time}s (attempt {attempt}/{MAX_RETRIES})")
        time.sleep(wait_time)
        page.reload()
        page.wait_for_load_state("networkidle")

    if is_error_page(page):
        log_event(run_log, f"Giving up on '{description}' after {MAX_RETRIES} retries")
        return False

    return True