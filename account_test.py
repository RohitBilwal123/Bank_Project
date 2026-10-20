
import pytest

from app import app, accounts


@pytest.fixture
def client():
    """Create a Flask test client and reset test accounts."""
    app.config["TESTING"] = True
    accounts.clear()

    with app.test_client() as test_client:
        yield test_client

    accounts.clear()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Bank Management System" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_version_endpoint(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json()["version"] == "2.0"


def test_create_account(client):
    response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 1000
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["accountType"] == "savings"
    assert data["balance"] == 1000
    assert data["accountNumber"]


def test_create_account_invalid_name(client):
    response = client.post(
        "/api/accounts",
        json={
            "name": "",
            "accountType": "savings",
            "initialBalance": 1000
        }
    )

    assert response.status_code == 400


def test_create_account_invalid_type(client):
    response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "invalid",
            "initialBalance": 1000
        }
    )

    assert response.status_code == 400


def test_create_account_negative_balance(client):
    response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": -100
        }
    )

    assert response.status_code == 400


def test_login_existing_account(client):
    create_response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 1000
        }
    )

    account_number = create_response.get_json()["accountNumber"]

    response = client.post(
        "/api/login",
        json={"accountNumber": account_number}
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful."


def test_login_nonexistent_account(client):
    response = client.post(
        "/api/login",
        json={"accountNumber": "999999999"}
    )

    assert response.status_code == 404


def test_account_details(client):
    create_response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 1500
        }
    )

    account_number = create_response.get_json()["accountNumber"]

    response = client.get(f"/api/accounts/{account_number}")

    assert response.status_code == 200
    assert response.get_json()["balance"] == 1500


def test_deposit_invalid_account(client):
    response = client.post(
        "/api/accounts/999999999/deposit",
        json={"amount": 100}
    )

    assert response.status_code == 404


def test_deposit_invalid_amount(client):
    create_response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 1000
        }
    )

    account_number = create_response.get_json()["accountNumber"]

    response = client.post(
        f"/api/accounts/{account_number}/deposit",
        json={"amount": -50}
    )

    assert response.status_code == 400


def test_withdraw_invalid_account(client):
    response = client.post(
        "/api/accounts/999999999/withdraw",
        json={"amount": 100}
    )

    assert response.status_code == 404


def test_withdraw_insufficient_balance(client):
    create_response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 100
        }
    )

    account_number = create_response.get_json()["accountNumber"]

    response = client.post(
        f"/api/accounts/{account_number}/withdraw",
        json={"amount": 500}
    )

    assert response.status_code == 400


def test_calculate_interest(client):
    create_response = client.post(
        "/api/accounts",
        json={
            "name": "Test User",
            "accountType": "savings",
            "initialBalance": 1000
        }
    )

    assert create_response.status_code == 201

    account_number = create_response.get_json()["accountNumber"]

    response = client.get(
        f"/api/accounts/{account_number}/interest"
    )

    assert response.status_code == 200

    data = response.get_json()

    # SavingsAccount applies 2% interest to the balance.
    assert data["balance"] == 1020
    assert data["interestAdded"] == 20
    assert data["interestRate"] == 0.02
