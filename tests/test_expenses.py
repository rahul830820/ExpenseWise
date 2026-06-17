def test_create_expense(client, auth_headers):

    category_response = client.post(
        "/categories",
        json={
            "name": "Food"
        },
        headers=auth_headers
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/expenses",
        json={
            "amount": 500,
            "description": "Lunch",
            "expense_date": "2026-06-15",
            "category_id": category_id
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["amount"] == 500
    assert data["description"] == "Lunch"