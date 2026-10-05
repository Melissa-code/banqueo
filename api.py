from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bank.bank import Bank
from bank.client import Client

app = FastAPI(title="Banqueo")
bank = Bank(1, "Banque Populaire")  #perdu à chaque redémarrage


class ClientIn(BaseModel):
    id: int
    firstname: str
    lastname: str


class AccountIn(BaseModel):
    account_name: str
    account_number: str
    initial_balance: Decimal = Decimal("0.00")


@app.post("/clients", status_code=201)
def create_client(data: ClientIn):
    try:
        client = bank.add_client(Client(data.id, data.firstname, data.lastname))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return {"id": client.id, "firstname": client.firstname, "lastname": client.lastname}


@app.post("/clients/{client_id}/accounts", status_code=201)
def open_account(client_id: int, data: AccountIn):
    try:
        client = bank.get_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    try:
        account = bank.open_account(
            client, data.account_name, data.account_number, data.initial_balance
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return {"account_number": account.account_number, "balance": str(account.balance)}


@app.get("/clients/{client_id}/balance")
def get_balance(client_id: int):
    try:
        client = bank.get_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"client_id": client.id, "total_balance": str(client.get_total_balance())}