def test_category_wise_report(client, auth_headers):

    category_response = client.post(
        "/categories",
        json={"name": "Food"},
        headers=auth_headers
    )

    category_id = category_response.json()["id"]

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "description": "Lunch",
            "expense_date": "2026-06-15",
            "category_id": category_id
        },
        headers=auth_headers
    )

    response = client.get(
        "/reports/category-wise",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"
    assert data[0]["total"] == 1000

def test_monthly_report(client, auth_headers):

    category_response = client.post(
        "/categories",
        json={"name": "Food"},
        headers=auth_headers
    )

    category_id = category_response.json()["id"]

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "description": "Lunch",
            "expense_date": "2026-06-15",
            "category_id": category_id
        },
        headers=auth_headers
    )

    response = client.get(
        "/reports/monthly",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["month"] == "2026-06"
    assert data[0]["total"] == 1000