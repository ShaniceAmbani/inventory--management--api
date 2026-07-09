import pytest
import app as app_module
import inventory

@pytest.fixture
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
    response = client.post("/inventory", json={"barcode": "123456789012", "price": 3.99, "stock": 5})
    assert response.status_code == 201

def test_create_item_requires_barcode_or_name(client):
    response = client.post("/inventory", json={"price": 2.5, "stock": 3})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Either barcode or product name is required"

def test_product_search_route(client):
    app_module.get_product_by_barcode = lambda barcode: {"barcode": barcode, "product_name": "Query Product"}
    response = client.get("/product?barcode=123456789012")
    assert response.status_code == 200