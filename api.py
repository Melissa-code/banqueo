from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bank.bank import Bank
from bank.client import Client

app = FastAPI(title="Banqueo")
bank = Bank(1, "Banque Populaire")  # perdu à chaque redémarrage


class ClientIn(BaseModel):
    id: int
    firstname: str
    lastname: str

class AccountIn(BaseModel):
    account_name: str
    account_number: str
    initial_balance: Decimal = Decimal("0.00")

class AmountIn(BaseModel):
    amount: Decimal


@app.get("/clients/{client_id}",
    summary="Obtenir un client par ID",
    description="Renvoie les informations d'un client par ID. Renvoie 404 si le client n'existe pas."
)
def get_client(client_id: int):
    try:
        client = bank.get_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"id": client.id, "firstname": client.firstname, "lastname": client.lastname}


@app.post("/clients", 
    status_code=201, 
    summary="Créer un client",
    description="Crée un client. Renvoie 409 si l'ID existe déjà."
)
def create_client(data: ClientIn):
    try:
        client = bank.add_client(Client(data.id, data.firstname, data.lastname))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return {"id": client.id, "firstname": client.firstname, "lastname": client.lastname}


@app.get("/clients/",
    summary="Lister tous les clients",
    description="Renvoie la liste de tous les clients."
)
def list_clients():
    return [
        {"id": client.id, "firstname": client.firstname, "lastname": client.lastname}
        for client in bank.get_all_clients()
    ]


@app.get("/accounts/{account_number}",
    summary="Obtenir un compte par numéro",
    description="Renvoie les informations d'un compte par numéro. Renvoie 404 si le compte n'existe pas."
)
def get_account(account_number: str):
    try:
        account = bank.get_account_by_number(account_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"account_name": account.account_name, "account_number": account.account_number, "balance": str(account.balance)}


@app.get("/accounts/",
    summary="Lister tous les comptes",
    description="Renvoie la liste de tous les comptes."
)
def list_accounts():
    return [
        {"account_number": account.account_number, "balance": str(account.balance)}
        for account in bank.get_all_accounts()
    ]


@app.post("/clients/{client_id}/accounts", 
    status_code=201, 
    summary="Ouvrir un compte pour un client",
    description="Ouvre un compte pour un client. Renvoie 404 si le client n'existe pas, 409 si le compte existe déjà."
)
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


@app.get("/clients/{client_id}/accounts",
    summary="Lister tous les comptes d'un client",
    description="Renvoie la liste de tous les comptes d'un client. Renvoie 404 si le client n'existe pas."
)
def list_client_accounts(client_id: int):
    try:
        client = bank.get_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return [
        {"account_number": account.account_number, "balance": str(account.balance)}
        for account in client.get_all_accounts()
    ]


@app.get("/clients/{client_id}/balance", 
    summary="Obtenir le solde total d'un client",
    description="Renvoie le solde total de tous les comptes d'un client. Renvoie 404 si le client n'existe pas."
)
def get_balance(client_id: int):
    try:
        client = bank.get_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"client_id": client.id, "total_balance": str(client.get_total_balance())}


@app.post("/accounts/{account_number}/deposit",
    summary="Déposer de l'argent",
    description="Dépose un montant sur un compte. 404 si le compte n'existe pas."
)
def deposit(account_number: str, data: AmountIn):
    try:
        account = bank.get_account_by_number(account_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    try:
        new_balance = account.deposit(data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"account_number": account_number, "balance": str(new_balance)}


@app.post("/accounts/{account_number}/withdraw",
          summary="Retirer de l'argent",
          description="Retire un montant d'un compte. 404 si le compte n'existe pas, 400 si le retrait est refusé.")
def withdraw(account_number: str, data: AmountIn):
    try:
        account = bank.get_account_by_number(account_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    try:
        new_balance = account.withdraw(data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"account_number": account_number, "balance": str(new_balance)}


@app.get("/accounts/{account_number}/history",
         summary="Historique d'un compte",
         description="Liste les opérations du compte. 404 si le compte n'existe pas.")
def history(account_number: str):
    try:
        account = bank.get_account_by_number(account_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return [
        {
            "date": str(op["date"]),
            "type": op["type"],
            "amount": str(op["amount"]),
            "balance": str(op["balance"]),
        }
        for op in account.get_history()
    ]


@app.delete("/clients/{client_id}",
    summary="Supprimer un client",
    description="Supprime un client et tous ses comptes. Renvoie 404 si le client n'existe pas."
)
def delete_client(client_id: int):
    try:
        bank.delete_client_by_id(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"message": f"Client avec l'ID {client_id} supprimé."}


@app.delete("/accounts/{account_number}",
    summary="Supprimer un compte",
    description="Supprime un compte. Renvoie 404 si le compte n'existe pas."
)   
def delete_account(account_number: str):
    try:
        bank.delete_account_by_number(account_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"message": f"Compte avec le numéro {account_number} supprimé."}
