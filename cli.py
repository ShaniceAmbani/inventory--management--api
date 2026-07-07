import requests

BASE_URL = "http://127.0.0.1:5000"


def view_all_items():
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=5)
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        print("INVENTORY")

        for item in items:
            print(f"""
ID: {item['id']}
Product: {item['product_name']}
Brand: {item['brand']}
Price: {item['price']}
Stock: {item['stock']}
Barcode: {item['barcode']}
""")
    else:
        print(response.json())


def view_one_item():
    item_id = input("Enter Item ID: ")

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}", timeout=5)
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        item = response.json()

        print(f"""
ID: {item['id']}
Product: {item['product_name']}
Brand: {item['brand']}
Price: {item['price']}
Stock: {item['stock']}
Barcode: {item['barcode']}

Ingredients:
{item['ingredients']}
""")
    else:
        print(response.json())


def add_item():
    barcode = input("Barcode: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    data = {
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=data,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 201:
        print("Item added successfully!")

    print(response.json())


def update_item():
    item_id = input("Item ID: ")

    print("Leave blank if you don't want to change a field.")

    price = input("New Price: ")
    stock = input("New Stock: ")

    updates = {}

    if price:
        try:
            updates["price"] = float(price)
        except ValueError:
            print("Invalid price.")
            return

    if stock:
        try:
            updates["stock"] = int(stock)
        except ValueError:
            print("Invalid stock.")
            return

    if not updates:
        print("Nothing to update.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=updates,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        print("Item updated successfully!")

    print(response.json())


def delete_item():
    item_id = input("Item ID: ")

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}",
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        print("Item deleted successfully!")

    print(response.json())


def search_api():
    barcode = input("Enter Barcode: ")

    try:
        response = requests.get(
            f"{BASE_URL}/product/{barcode}",
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Could not connect to the Flask server.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200:
        product = response.json()

        print(f"""PRODUCT FOUND
Product Name : {product['product_name']}
Brand        : {product['brand']}
Ingredients  : {product['ingredients']}
""")
    else:
        print(response.json())


def menu():
    while True:
        print("""Inventory Management System

1. View All Inventory
2. View One Item
3. Add Item
4. Update Item
5. Delete Item
6. Search OpenFoodFacts
7. Exit
""")

        choice = input("Select an option: ")

        if choice == "1":
            view_all_items()

        elif choice == "2":
            view_one_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            search_api()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()