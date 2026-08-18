import json
import os
from datetime import datetime

RUNS_DIR = os.path.join(os.path.dirname(__file__), "..", "runs")


def new_run_log():
    return {
        "started_at": datetime.now().isoformat(),
        "events": [],
        "items_processed": 0,
        "disruptions_encountered": 0,
        "retries": 0
    }


def log_event(run_log, message):
    entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    run_log["events"].append(entry)
    print(entry)


def save_screenshot(page, run_log, name):
    os.makedirs(RUNS_DIR, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.png"
    path = os.path.join(RUNS_DIR, filename)
    page.screenshot(path=path)
    log_event(run_log, f"Screenshot saved: {filename}")
    return filename


def finish_run(run_log):
    run_log["finished_at"] = datetime.now().isoformat()

    summary = (
        f"\n--- RUN SUMMARY ---\n"
        f"Items processed: {run_log['items_processed']}\n"
        f"Disruptions encountered: {run_log['disruptions_encountered']}\n"
        f"Retries: {run_log['retries']}\n"
        f"Started: {run_log['started_at']}\n"
        f"Finished: {run_log['finished_at']}\n"
    )
    print(summary)
    run_log["summary_text"] = summary

    os.makedirs(RUNS_DIR, exist_ok=True)
    log_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_run_log.json"
    log_path = os.path.join(RUNS_DIR, log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(run_log, f, indent=2)
    print(f"Full run log saved to: {log_filename}")