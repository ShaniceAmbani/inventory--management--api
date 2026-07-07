inventory = [
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


# GET ALL ITEMS
def get_all_items():
    "Return all inventory items."
    return inventory


# GET ITEM BY ID
def get_item_by_id(item_id):
    "Return one inventory item by ID."

    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


# ADD ITEM
def add_item(item):
    "Add a new inventory item."

    new_id = inventory[-1]["id"] + 1 if inventory else 1

    item["id"] = new_id
    inventory.append(item)

    return item


# UPDATE ITEM
def update_item(item_id, updates):
    "Update an existing inventory item."

    item = get_item_by_id(item_id)

    if item is None:
        return None

    for key, value in updates.items():
        if key != "id" and key in item:
            item[key] = value

    return item


# DELETE ITEM
def delete_item(item_id):
    "Delete an inventory item."

    item = get_item_by_id(item_id)

    if item is None:
        return False

    inventory.remove(item)

    return True