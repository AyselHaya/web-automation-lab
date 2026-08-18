import time

MAX_RETRIES = 5


def is_error_page(page):
    try:
        return "Internal Server Error" in page.content()
    except Exception:
        return False


def with_retry(action, page, run_log, log_event, description):
    """
    Runs `action()`. If it fails (either the action itself throws, e.g.
    because an element never appears on an error page, or the resulting
    page is a simulated error page), reloads with exponential backoff and
    tries again, up to MAX_RETRIES times.
    Returns True if it eventually succeeded, False if it never did.
    """
    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            action()
            page.wait_for_load_state("networkidle")
            if not is_error_page(page):
                return True
        except Exception as e:
            log_event(run_log, f"Action failed during '{description}': {type(e).__name__}")

        attempt += 1
        if attempt > MAX_RETRIES:
            break

        run_log["retries"] += 1
        run_log["disruptions_encountered"] += 1
        wait_time = min(2 ** attempt, 10)
        log_event(run_log, f"Retrying '{description}' in {wait_time}s (attempt {attempt}/{MAX_RETRIES})")
        time.sleep(wait_time)
        try:
            page.reload()
            page.wait_for_load_state("networkidle")
        except Exception:
            pass

    log_event(run_log, f"Giving up on '{description}' after {MAX_RETRIES} retries")
    return False