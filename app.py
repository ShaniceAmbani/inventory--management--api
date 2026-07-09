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
    return jsonify({"message": "Inventory Management API is running!"}), 200

@app.route("/inventory", methods=["GET"])
def inventory_list():
    return jsonify(get_all_items()), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def inventory_item(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body is required"}), 400

    barcode = data.get("barcode")
    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not barcode and not name:
        return jsonify({"error": "Either barcode or product name is required"}), 400

    product = get_product_by_barcode(barcode) if barcode else get_product_by_name(name)
    if not product:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

    try:
        new_item = {
            "barcode": product.get("barcode") or barcode,
            "product_name": product["product_name"],
            "brand": product["brand"],
            "ingredients": product["ingredients"],
            "price": float(price),
            "stock": int(stock),
        }
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number and stock must be an integer"}), 400

    added = add_item(new_item)
    return jsonify({"message": "Item added successfully", "item": added}), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def edit_item(item_id):
    data = request.get_json(silent=True)
    updated = update_item(item_id, data)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item updated successfully", "item": updated}), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted = delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted successfully"}), 200

@app.route("/product", methods=["GET"])
def search_product():
    barcode = request.args.get("barcode")
    product_name = request.args.get("name")
    product = get_product_by_barcode(barcode) if barcode else get_product_by_name(product_name)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

if __name__ == "__main__":
    app.run(debug=True)