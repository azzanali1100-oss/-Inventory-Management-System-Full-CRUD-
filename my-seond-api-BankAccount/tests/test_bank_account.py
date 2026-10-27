import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine, select

from app.main import app
from app.schemas.bank_account import CreateAccountRequest, DepositRequest
import app.services.bank_account_services as bank_account_services
from app.services.bank_account_services import (
    create_account,
    deposit,
    get_account,
    transfer,
    withdraw,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    test_engine = create_engine(
        URL.create("sqlite", database=str(tmp_path / "test_accounts.db")),
        connect_args={"check_same_thread": False},
    )
    monkeypatch.setattr(bank_account_services, "engine", test_engine)
    bank_account_services.initialize_database()
    yield
    test_engine.dispose()


def test_create_account_and_deposit():
    result = create_account("Sara", 1000)
    assert result == {"owner": "Sara", "balance": 1000}

    result = deposit("Sara", 500)
    assert result["new_balance"] == 1500
    assert get_account("Sara")["balance"] == 1500


def test_withdraw_and_transfer():
    create_account("Sara", 1000)
    create_account("Ali", 200)

    result = withdraw("Sara", 300)
    assert result["new_balance"] == 700

    transfer_result = transfer("Sara", "Ali", 200)
    assert transfer_result["from_balance"] == 500
    assert transfer_result["to_balance"] == 400


def test_validation_rejects_bad_amount():
    with pytest.raises(ValidationError):
        DepositRequest(owner="Sara", amount="five")


def test_request_schema_accepts_default_balance():
    request = CreateAccountRequest(owner="Ali")
    assert request.balance == 0


def test_missing_account_returns_not_found():
    response = client.get("/account/Sara")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account for Sara not found."}


def test_duplicate_account_returns_conflict():
    client.post("/account/create", json={"owner": "Sara", "balance": 100})

    response = client.post("/account/create", json={"owner": "Sara", "balance": 100})

    assert response.status_code == 409
    assert response.json() == {"detail": "Account for Sara already exists."}


def test_api_rejects_negative_amount():
    response = client.post("/account/deposit", json={"owner": "Sara", "amount": -1})

    assert response.status_code == 422


def test_health_endpoint_reports_api_ready():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_account_data_persists_and_is_listed_from_database():
    create_account("Sara", 250)

    with bank_account_services.engine.connect() as connection:
        stored_account = connection.execute(
            select(bank_account_services.accounts_table).where(
                bank_account_services.accounts_table.c.owner == "Sara"
            )
        ).mappings().one()

    response = client.get("/account")

    assert dict(stored_account) == {"owner": "Sara", "balance": 250}
    assert response.status_code == 200
    assert response.json() == [{"owner": "Sara", "balance": 250}]
