from typing import Optional

from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    owner: str = Field(min_length=1)
    balance: int = Field(default=0, ge=0)


class DepositRequest(BaseModel):
    owner: str = Field(min_length=1)
    amount: int = Field(ge=1)


class WithdrawRequest(BaseModel):
    owner: str = Field(min_length=1)
    amount: int = Field(ge=1)


class TransferRequest(BaseModel):
    from_owner: str = Field(min_length=1)
    to_owner: str = Field(min_length=1)
    amount: int = Field(ge=1)


class AccountResponse(BaseModel):
    owner: str
    balance: int


class MessageResponse(BaseModel):
    message: str
    owner: Optional[str] = None
    new_balance: Optional[int] = None
    from_balance: Optional[int] = None
    to_balance: Optional[int] = None


if __name__ == "__main__":
    req1 = CreateAccountRequest(owner="Sara", balance=1000)
    print(req1)
    req2 = DepositRequest(owner="Sara", amount=500)
    print(req2)
    req3 = TransferRequest(from_owner="Sara", to_owner="Ali", amount=200)
    print(req3)

    try:
        bad_req = DepositRequest(owner="Sara", amount="five")
        print(bad_req)
    except Exception as exc:  # pragma: no cover
        print("Validation Error:", exc)
