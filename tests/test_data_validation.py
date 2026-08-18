import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "sandbox_site", "data", "items.json")

REQUIRED_FIELDS = {"id", "title", "author", "genre", "price", "rating", "description"}


def load_items():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_items_file_has_data():
    items = load_items()
    assert len(items) >= 20, "Expected at least 20 dummy items"


def test_all_items_have_required_fields():
    items = load_items()
    for item in items:
        missing = REQUIRED_FIELDS - set(item.keys())
        assert not missing, f"Item {item.get('id')} missing fields: {missing}"


def test_all_ids_are_unique():
    items = load_items()
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), "Duplicate item IDs found"


def test_prices_are_positive():
    items = load_items()
    for item in items:
        assert item["price"] > 0, f"Item {item['id']} has non-positive price"