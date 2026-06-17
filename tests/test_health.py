from tests.conftest import client

def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "status": "success",
        "message": "ExpenseWise API Running"
    }