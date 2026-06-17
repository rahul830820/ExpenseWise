from tests.conftest import client

def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "test4@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test4@example.com"
    assert data["full_name"] == "Test User"


def test_login_user(client):

    client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"