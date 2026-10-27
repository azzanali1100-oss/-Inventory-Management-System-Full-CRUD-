from fastapi import APIRouter, HTTPException

from app.schemas.bank_account import (
    AccountResponse,
    CreateAccountRequest,
    DepositRequest,
    MessageResponse,
    TransferRequest,
    WithdrawRequest,
)
from app.services.bank_account_services import (
    create_account,
    deposit,
    get_account,
    list_accounts,
    transfer,
    withdraw,
)

router = APIRouter(prefix="/account", tags=["Bank Account"])


def _handle_service_result(result: dict):
    error = result.get("error")
    if error:
        if "not found" in error:
            status_code = 404
        elif "already exists" in error:
            status_code = 409
        else:
            status_code = 400
        raise HTTPException(status_code=status_code, detail=error)
    return result


@router.get("", response_model=list[AccountResponse])
def list_accounts_route():
    return list_accounts()


@router.get("/{owner}", response_model=AccountResponse)
def get_account_route(owner: str):
    return _handle_service_result(get_account(owner))


@router.post("/create", response_model=AccountResponse)
def create_account_route(request: CreateAccountRequest):
    return _handle_service_result(create_account(request.owner, request.balance))


@router.post("/deposit", response_model=MessageResponse)
def deposit_route(request: DepositRequest):
    return _handle_service_result(deposit(request.owner, request.amount))


@router.post("/withdraw", response_model=MessageResponse)
def withdraw_route(request: WithdrawRequest):
    return _handle_service_result(withdraw(request.owner, request.amount))


@router.post("/transfer", response_model=MessageResponse)
def transfer_route(request: TransferRequest):
    return _handle_service_result(transfer(request.from_owner, request.to_owner, request.amount))


if __name__ == "__main__":
    print(create_account_route(CreateAccountRequest(owner="Sara", balance=1000)))
    print(deposit_route(DepositRequest(owner="Sara", amount=500)))
    print(withdraw_route(WithdrawRequest(owner="Sara", amount=300)))
    print(transfer_route(TransferRequest(from_owner="Sara", to_owner="Ali", amount=200)))
