def test_budget_analysis(client, auth_headers):

    category_response = client.post(
        "/categories",
        json={"name": "Food"},
        headers=auth_headers
    )

    category_id = category_response.json()["id"]

    client.post(
        "/budgets",
        json={
            "amount": 5000,
            "category_id": category_id
        },
        headers=auth_headers
    )

    client.post(
        "/expenses",
        json={
            "amount": 2000,
            "description": "Groceries",
            "expense_date": "2026-06-15",
            "category_id": category_id
        },
        headers=auth_headers
    )

    response = client.get(
        "/budgets/analysis",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"
    assert data[0]["budget"] == 5000
    assert data[0]["spent"] == 2000
    assert data[0]["remaining"] == 3000
    assert data[0]["status"] == "Within Budget"