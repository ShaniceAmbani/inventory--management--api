import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product/"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


# HELPER FUNCTION
def _normalize_product(product_data, barcode=None):
    "Convert OpenFoodFacts data into a consistent format."

    if not product_data:
        return None

    return {
        "barcode": barcode or product_data.get("code") or "Unknown",
        "product_name": (
            product_data.get("product_name")
            or product_data.get("product_name_en")
            or "Unknown"
        ),
        "brand": (
            product_data.get("brands")
            or product_data.get("brand")
            or "Unknown"
        ),
        "ingredients": (
            product_data.get("ingredients_text")
            or "Not available"
        ),
    }


# SEARCH BY BARCODE
def get_product_by_barcode(barcode):
    "Fetch product details using a barcode."

    if not barcode:
        return None

    url = f"{BASE_URL}{barcode}.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        return _normalize_product(
            data.get("product", {}),
            barcode
        )

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None


# SEARCH BY PRODUCT NAME
def get_product_by_name(name):
    "Search OpenFoodFacts by product name."

    if not name:
        return None

    params = {
        "search_terms": name,
        "search_simple": 1,
        "json": 1,
        "action": "process",
    }

    try:
        response = requests.get(
            SEARCH_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        if not products:
            return None

        return _normalize_product(
            products[0],
            products[0].get("code")
        )

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None


# TEST THE FILE
if __name__ == "__main__":

    query = input("Enter barcode or product name: ")

    if query.isdigit():
        product = get_product_by_barcode(query)
    else:
        product = get_product_by_name(query)

    if product:
        print("\nProduct Found!\n")
        print(product)
    else:
        print("\nProduct not found.")