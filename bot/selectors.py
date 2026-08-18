# Centralized selectors for the bot — keeps all element-finding logic in one place,
# so if the site's DOM changes, we only update it here.

SEARCH_INPUT = "input[name='q']"
SEARCH_SUBMIT = "button[type='submit']"
BOOK_LINKS = "ul li a"
BORROW_BUTTON = "#borrow-btn"
BORROWER_NAME_INPUT = "#borrower-name"
CONFIRM_BORROW_BUTTON = "#confirm-borrow"
CONFIRMATION_TEXT = "#confirmation"