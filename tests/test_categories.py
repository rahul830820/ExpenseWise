def test_create_category(client, auth_headers):

    response = client.post("/categories", json={"name": "Food"}, headers=auth_headers)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Food"


def test_get_categories(client, auth_headers):

    client.post("/categories", json={"name": "Food"}, headers=auth_headers)

    response = client.get("/categories", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Food"
