import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bot"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bot", "handlers"))

from handlers.resilience import is_error_page


class FakePage:
    """Minimal fake Playwright page for unit testing is_error_page without a real browser."""
    def __init__(self, content_text):
        self._content = content_text

    def content(self):
        return self._content


def test_is_error_page_detects_error():
    page = FakePage("<html><body>Internal Server Error (simulated)</body></html>")
    assert is_error_page(page) is True


def test_is_error_page_normal_page():
    page = FakePage("<html><body>Welcome to BookNook</body></html>")
    assert is_error_page(page) is False


def test_retry_backoff_calculation():
    # Mirrors the backoff formula used in with_retry(): min(2 ** attempt, 10)
    assert min(2 ** 1, 10) == 2
    assert min(2 ** 2, 10) == 4
    assert min(2 ** 3, 10) == 8
    assert min(2 ** 4, 10) == 10  # capped
    assert min(2 ** 5, 10) == 10  # still capped