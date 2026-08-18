from handlers.resilience import is_error_page


def handle_redirect_if_present(page, run_log, log_event):
    promo_heading = page.locator("text=Limited Time Offer")
    if promo_heading.count() > 0:
        log_event(run_log, "Detected redirect to promo page — routing back")
        run_log["disruptions_encountered"] += 1
        back_link = page.locator("a", has_text="No thanks")
        back_link.click()
        page.wait_for_load_state("networkidle")
        log_event(run_log, "Routed back to intended page")
        return True
    return False


def ensure_reached_detail_page(page, run_log, log_event, solve_captcha_fn, max_loops=8):
    """
    Keeps resolving whatever's in the way — redirect, captcha, or a simulated
    server error — in whatever order they appear, until the real detail page
    (borrow button present) is reached, or gives up.
    """
    for _ in range(max_loops):
        if page.locator("#borrow-btn").count() > 0:
            return True

        if is_error_page(page):
            log_event(run_log, "Detected server error while reaching detail page — reloading")
            run_log["disruptions_encountered"] += 1
            run_log["retries"] += 1
            page.reload()
            page.wait_for_load_state("networkidle")
            continue

        redirected = handle_redirect_if_present(page, run_log, log_event)
        if redirected:
            continue

        solved = solve_captcha_fn(page, run_log, log_event)
        if solved:
            continue

        page.wait_for_load_state("networkidle")

    return page.locator("#borrow-btn").count() > 0