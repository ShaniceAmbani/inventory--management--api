from unittest.mock import patch

import openfoodfacts


def test_get_product_by_barcode_returns_normalized_payload():
    fake_response = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds",
        },
    }

    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = fake_response

        product = openfoodfacts.get_product_by_barcode("737628064502")

    assert product is not None
    assert product["barcode"] == "737628064502"
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["ingredients"] == "Filtered water, almonds"


def test_get_product_by_barcode_returns_none_for_missing_product():
    fake_response = {
        "status": 0,
        "product": None,
    }

    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = fake_response

        product = openfoodfacts.get_product_by_barcode("000000000000")

    assert product is None


def test_get_product_by_name_returns_product():
    fake_response = {
        "products": [
            {
                "code": "737628064502",
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds",
            }
        ]
    }

    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = fake_response

        product = openfoodfacts.get_product_by_name("almond")

    assert product is not None
    assert product["barcode"] == "737628064502"
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"


def test_get_product_by_name_returns_none_when_not_found():
    fake_response = {
        "products": []
    }

    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = fake_response

        product = openfoodfacts.get_product_by_name("abcdefg")

    assert product is None