import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    MetaData,
    String,
    Table,
    URL,
    create_engine,
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

metadata = MetaData()
accounts_table = Table(
    "accounts",
    metadata,
    Column("owner", String(255), primary_key=True),
    Column("balance", BigInteger, nullable=False),
    CheckConstraint("balance >= 0", name="check_account_balance_nonnegative"),
)

database_host = os.getenv("BANK_DB_HOST")
if database_host:
    database_url = URL.create(
        "mysql+pymysql",
        username=os.getenv("BANK_DB_USER", "root"),
        password=os.getenv("BANK_DB_PASSWORD") or None,
        host=database_host,
        port=int(os.getenv("BANK_DB_PORT", "3306")),
        database=os.getenv("BANK_DB_NAME", "bank_accounts"),
    )
else:
    database_url = URL.create(
        "sqlite",
        database=str(PROJECT_ROOT / "bank_accounts.db"),
    )

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False}
    if database_url.get_backend_name() == "sqlite"
    else {},
    pool_pre_ping=True,
)


def initialize_database():
    metadata.create_all(engine)


initialize_database()


def create_account(owner: str, balance: int = 0):
    if balance < 0:
        return {"error": "Balance cannot be negative."}

    try:
        with engine.begin() as connection:
            connection.execute(
                insert(accounts_table).values(owner=owner, balance=balance)
            )
    except IntegrityError:
        return {"error": f"Account for {owner} already exists."}
    return {"owner": owner, "balance": balance}


def get_account(owner: str):
    with engine.connect() as connection:
        account = connection.execute(
            select(accounts_table.c.owner, accounts_table.c.balance).where(
                accounts_table.c.owner == owner
            )
        ).mappings().first()
    if account is None:
        return {"error": f"Account for {owner} not found."}
    return dict(account)


def list_accounts():
    with engine.connect() as connection:
        accounts = connection.execute(
            select(accounts_table.c.owner, accounts_table.c.balance).order_by(
                accounts_table.c.owner
            )
        ).mappings().all()
    return [dict(account) for account in accounts]


def deposit(owner: str, amount: int):
    if amount <= 0:
        return {"error": "Amount must be positive."}

    with engine.begin() as connection:
        account = connection.execute(
            select(accounts_table.c.balance)
            .where(accounts_table.c.owner == owner)
            .with_for_update()
        ).mappings().first()
        if account is None:
            return {"error": f"Account for {owner} not found."}
        new_balance = account["balance"] + amount
        connection.execute(
            update(accounts_table)
            .where(accounts_table.c.owner == owner)
            .values(balance=new_balance)
        )
    return {
        "message": f"{amount} deposited.",
        "owner": owner,
        "new_balance": new_balance,
    }


def withdraw(owner: str, amount: int):
    if amount <= 0:
        return {"error": "Amount must be positive."}

    with engine.begin() as connection:
        account = connection.execute(
            select(accounts_table.c.balance)
            .where(accounts_table.c.owner == owner)
            .with_for_update()
        ).mappings().first()
        if account is None:
            return {"error": f"Account for {owner} not found."}
        if amount > account["balance"]:
            return {"error": "Insufficient funds."}
        new_balance = account["balance"] - amount
        connection.execute(
            update(accounts_table)
            .where(accounts_table.c.owner == owner)
            .values(balance=new_balance)
        )
    return {
        "message": f"{amount} withdrawn.",
        "owner": owner,
        "new_balance": new_balance,
    }


def transfer(from_owner: str, to_owner: str, amount: int):
    if amount <= 0:
        return {"error": "Amount must be positive."}

    with engine.begin() as connection:
        accounts = connection.execute(
            select(accounts_table.c.owner, accounts_table.c.balance)
            .where(accounts_table.c.owner.in_((from_owner, to_owner)))
            .order_by(accounts_table.c.owner)
            .with_for_update()
        ).mappings().all()
        account_balances = {
            account["owner"]: account["balance"] for account in accounts
        }

        if from_owner not in account_balances:
            return {"error": f"Account for {from_owner} not found."}
        if to_owner not in account_balances:
            return {"error": f"Account for {to_owner} not found."}
        if amount > account_balances[from_owner]:
            return {"error": "Insufficient funds."}

        from_balance = account_balances[from_owner] - amount
        to_balance = account_balances[to_owner] + amount
        connection.execute(
            update(accounts_table)
            .where(accounts_table.c.owner == from_owner)
            .values(balance=from_balance)
        )
        connection.execute(
            update(accounts_table)
            .where(accounts_table.c.owner == to_owner)
            .values(balance=to_balance)
        )
    return {
        "message": f"{amount} transferred from {from_owner} to {to_owner}.",
        "from_balance": from_balance,
        "to_balance": to_balance,
    }


if __name__ == "__main__":
    print(create_account("Sara", 1000))
    print(create_account("Ali", 0))
    print(deposit("Sara", 500))
    print(withdraw("Sara", 300))
    print(withdraw("Sara", 5000))
    print(transfer("Sara", "Ali", 200))
    print(get_account("Sara"))
    print(get_account("Ali"))
