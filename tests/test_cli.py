from unittest.mock import patch

import cli


class:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


def test_view_all_items_prints_inventory():
    def fake_get(url, timeout=5):
        return (
            [
                {
                    "id": 1,
                    "product_name": "Milk",
                    "brand": "Brand",
                    "price": 2.5,
                    "stock": 4,
                    "barcode": "123",
                }
            ]
        )

    (cli.requests, "get", fake_get)

    cli.view_all_items()

    captured = ()

    assert "INVENTORY" in captured
    assert "Milk" in captured
    assert "Brand" in captured


def test_add_item_sends_expected_payload():
    answers = ["123456789012", "3.49", "7"]

    sent_payload = {}

    def fake_input(prompt=""):
        return answers.pop(0)

    def fake_post(url, json=None, timeout=5):
        sent_payload["url"] = url
        sent_payload["json"] = json
        return(
            {
                "message": "Item added successfully"
            },
            status_code=201,
        )

    (cli, "input", fake_input)
    (cli.requests, "post", fake_post)

    cli.add_item()

    assert sent_payload["url"] == f"{cli.BASE_URL}/inventory"
    assert sent_payload["json"] == {
        "barcode": "123456789012",
        "price": 3.49,
        "stock": 7,
    }