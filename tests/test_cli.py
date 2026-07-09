def test_add_item_sends_expected_payload():
    # UPDATED: Added "BrandName" as the 4th input
    answers = ["123456789012", "3.49", "7", "BrandName"]
    
    sent_payload = {}

    def fake_input(prompt=""):
        return answers.pop(0)

    def fake_post(url, json=None, timeout=5):
        sent_payload["url"] = url
        sent_payload["json"] = json
        return FakeResponse({"message": "Item added successfully"}, status_code=201)

    with patch("builtins.input", side_effect=fake_input), patch(
        "cli.requests.post", side_effect=fake_post
    ):
        cli.add_item()

    # UPDATED: Assert that the payload includes the brand
    assert sent_payload["json"] == {
        "barcode": "123456789012",
        "price": 3.49,
        "stock": 7,
        "brand": "BrandName"
    }