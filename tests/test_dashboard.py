def test_dashboard_summary(client, auth_headers):

    category_response = client.post(
        "/categories", json={"name": "Food"}, headers=auth_headers
    )

    category_id = category_response.json()["id"]

    client.post(
        "/incomes",
        json={"amount": 80000, "source": "Salary", "income_date": "2026-06-01"},
        headers=auth_headers,
    )

    client.post(
        "/expenses",
        json={
            "amount": 5000,
            "description": "Groceries",
            "expense_date": "2026-06-15",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    response = client.get("/dashboard/summary", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 80000
    assert data["total_expenses"] == 5000
    assert data["savings"] == 75000
    assert data["savings_rate"] == 93.75
    assert data["expense_count"] == 1
    assert data["category_count"] == 1
