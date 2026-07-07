import pytest

import app as app_module
import inventory


@pytest.fixture(True)
def reset_inventory():
    inventory.inventory[:] = [
        {
            "id": 1,
            "barcode": "737628064502",
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "price": 450,
            "stock": 20,
            "ingredients": "Filtered water, almonds, cane sugar",
        }
    ]


    inventory.inventory[:] = [
        {
            "id": 1,
            "barcode": "737628064502",
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "price": 450,
            "stock": 20,
            "ingredients": "Filtered water, almonds, cane sugar",
        }
    ]


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as client:
        yield client


def test_inventory_crud_flow(client):

    app_module.get_product_by_barcode = lambda barcode: {
        "barcode": barcode,
        "product_name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "Test Ingredients",
    }

    # CREATE
    response = client.post(
        "/inventory",
        json={
            "barcode": "123456789012",
            "price": 3.99,
            "stock": 5,
        },
    )

    assert response.status_code == 201

    created = response.get_json()["item"]

    assert created["product_name"] == "Test Product"
    assert created["stock"] == 5

    # GET ALL
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # GET ONE
    response = client.get(f"/inventory/{created['id']}")

    assert response.status_code == 200

    # UPDATE
    response = client.patch(
        f"/inventory/{created['id']}",
        json={
            "price": 4.25,
            "stock": 8,
        },
    )

    assert response.status_code == 200

    updated = response.get_json()["item"]

    assert updated["price"] == 4.25
    assert updated["stock"] == 8

    # DELETE
    response = client.delete(f"/inventory/{created['id']}")

    assert response.status_code == 200

    # CONFIRM DELETE
    response = client.get(f"/inventory/{created['id']}")

    assert response.status_code == 404


def test_create_item_requires_barcode_or_name(client):

    response = client.post(
        "/inventory",
        json={
            "price": 2.5,
            "stock": 3,
        },
    )

    assert response.status_code == 400

    assert (
        response.get_json()["error"] == "Either barcode or product name is required"
    )


def test_product_search_route(client):

    app_module.get_product_by_barcode = lambda barcode: {
        "barcode": barcode,
        "product_name": "Query Product",
        "brand": "Query Brand",
        "ingredients": "Query Ingredients",
    }

    response = client.get("/product?barcode=123456789012")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Query Product"