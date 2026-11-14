import re
from decimal import Decimal

import requests

import utils

API = utils.API

NAME_ACCOUNT_PATTERN = re.compile(r"^[A-Z0-9a-zÀ-ÖØ-öø-ÿ' -]+$")

NAME_ACCOUNT_VALIDATE = (
    NAME_ACCOUNT_PATTERN.pattern,
    "Lettres, chiffres, espaces, apostrophes et tirets uniquement.",
)


# ======== Create account for client =======

def get_account_types() -> dict[str, Decimal]:
    """Demande à l'API les types de compte et leur plafond"""
    try:
        r = requests.get(f"{utils.API}/account-types", timeout=5)
    except requests.RequestException:
        return {}

    if not r.ok:
        return {}
    return {name: Decimal(cap) for name, cap in r.json().items()}


def validate_account(client_id: int, account_name: str, account_number: str) -> str | None:
    """Renvoie un message d'erreur"""
    if client_id is None or not account_number.strip() or not account_name.strip():
        return "Tous les champs sont obligatoires"
    if not NAME_ACCOUNT_PATTERN.fullmatch(account_number.strip()) or not NAME_ACCOUNT_PATTERN.fullmatch(account_name.strip()):
        return "Les nom et numéro de compte ne doivent contenir que des lettres et chiffres."
    return None

def create_account(
        client_id: int, 
        account_name: str, 
        account_number: str, 
        initial_balance: Decimal
      ) -> tuple[bool, str]:
    """Appel à API => Renvoie succès message"""
    try:
        r = requests.post(f"{utils.API}/clients/{client_id}/accounts", json={
            "id": int(client_id),
            "account_number": account_number.strip(),
            "account_name": account_name.strip(),
        }, timeout=5)
    except requests.RequestException:
        return False, "Connexion à l'API impossible"

    if r.status_code == 201:
        return True, f"Le compte {account_name} n° {account_number} a été ouvert avec succès"
    return False, utils.error_message(r)