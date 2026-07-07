# Inventory Management API

A simple Flask REST API for managing inventory items. The project also uses the OpenFoodFacts API to fetch product details by barcode or product name and includes a CLI for interacting with the API.

## Features

- View all inventory items
- View one inventory item
- Add a new item
- Update an item
- Delete an item
- Search products using the OpenFoodFacts API
- CLI for interacting with the API
- Unit tests using pytest

## Installation

1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Flask application:

```bash
python app.py
```

## Using the CLI

Run:

```bash
python cli.py
```

## API Endpoints

- `GET /inventory` - View all items
- `GET /inventory/<id>` - View one item
- `POST /inventory` - Add a new item
- `PATCH /inventory/<id>` - Update an item
- `DELETE /inventory/<id>` - Delete an item
- `GET /product?barcode=<barcode>` - Search by barcode
- `GET /product?name=<product_name>` - Search by product name

## Running Tests

Run all tests with:

```bash
pytest
```

or

```bash
pytest -q
```
