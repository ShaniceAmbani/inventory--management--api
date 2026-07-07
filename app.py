from flask import Flask, jsonify, request

from inventory import (
    add_item,
    delete_item,
    get_all_items,
    get_item_by_id,
    update_item,
)
from openfoodfacts import get_product_by_barcode, get_product_by_name

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"Inventory Management API is running!"}), 200


# GET ALL INVENTORY
@app.route("/inventory", methods=["GET"])
def inventory_list():
    return jsonify(get_all_items()), 200


# GET ONE INVENTORY ITEM
@app.route("/inventory/<int:item_id>", methods=["GET"])
def inventory_item(item_id):
    item = get_item_by_id(item_id)

    if item is None:
        return jsonify({"Item not found"}), 404

    return jsonify(item), 200


# ADD ITEM
@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"Request body is required"}), 400

    if not isinstance(data, dict):
        return jsonify({"JSON object required"}), 400

    barcode = data.get("barcode")
    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not barcode and not name:
        return jsonify({
            "Either barcode or product name is required"
        }), 400

    if price is None:
        return jsonify({"Price is required"}), 400

    if stock is None:
        return jsonify({"Stock is required"}), 400

    try:
        price = float(price)
        stock = int(stock)
    except (TypeError, ValueError):
        return jsonify({
            "Price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        return jsonify({"Price cannot be negative"}), 400

    if stock < 0:
        return jsonify({"Stock cannot be negative"}), 400

    if barcode:
        product = get_product_by_barcode(barcode)
    else:
        product = get_product_by_name(name)

    if product is None:
        return jsonify({
            "Product not found in OpenFoodFacts"
        }), 404

    new_item = {
        "barcode": product.get("barcode") or barcode,
        "product_name": product["product_name"],
        "brand": product["brand"],
        "ingredients": product["ingredients"],
        "price": price,
        "stock": stock,
    }

    added = add_item(new_item)

    return jsonify({
        "Item added successfully",
        "item": added
    }), 201


# UPDATE ITEM
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def edit_item(item_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"No update data provided"}), 400

    if not isinstance(data, dict):
        return jsonify({"JSON object required"}), 400

    if "id" in data:
        return jsonify({"ID cannot be updated"}), 400

    if "price" in data:
        try:
            data["price"] = float(data["price"])

            if data["price"] < 0:
                return jsonify({"Price cannot be negative"}), 400

        except (TypeError, ValueError):
            return jsonify({
                "Price must be a valid number"
            }), 400

    if "stock" in data:
        try:
            data["stock"] = int(data["stock"])

            if data["stock"] < 0:
                return jsonify({"Stock cannot be negative"}), 400

        except (TypeError, ValueError):
            return jsonify({
                "Stock must be a valid integer"
            }), 400

    updated = update_item(item_id, data)

    if updated is None:
        return jsonify({"Item not found"}), 404

    return jsonify({
        "Item updated successfully",
        "item": updated
    }), 200


# DELETE ITEM
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted = delete_item(item_id)

    if not deleted:
        return jsonify({"Item not found"}), 404

    return jsonify({
        "Item deleted successfully"
    }), 200


# SEARCH OPENFOODFACTS
@app.route("/product", methods=["GET"])
@app.route("/product/<path:identifier>", methods=["GET"])
def search_product(identifier=None):

    barcode = request.args.get("barcode")
    product_name = request.args.get("name") or request.args.get("query")

    if not barcode and not product_name and identifier:
        barcode = identifier

    if barcode:
        product = get_product_by_barcode(barcode)

    elif product_name:
        product = get_product_by_name(product_name)

    else:
        return jsonify({
            "Barcode or product name is required"
        }), 400

    if product is None:
        return jsonify({
            "Product not found"
        }), 404

    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)