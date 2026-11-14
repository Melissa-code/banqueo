import re

import requests

import utils

API = utils.API

NAME_PATTERN = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$")

NAME_VALIDATE = (
    NAME_PATTERN.pattern,
    "Lettres, espaces, apostrophes et tirets uniquement.",
)

# ======== Create client =======

def validate_client(client_id: int, lastname: str, firstname: str) -> str | None:
    """Renvoie un message d'erreur"""
    if client_id is None or not lastname.strip() or not firstname.strip():
        return "Tous les champs sont obligatoires"
    if not NAME_PATTERN.fullmatch(lastname.strip()) or not NAME_PATTERN.fullmatch(firstname.strip()):
        return "Le nom et le prénom ne doivent contenir que des lettres."
    return None

def create_client(client_id: int, lastname: str, firstname: str) -> tuple[bool, str]:
    """Appel à API => Renvoie succès message"""
    try:
        r = requests.post(f"{utils.API}/clients", json={
            "id": int(client_id),
            "lastname": lastname.strip(),
            "firstname": firstname.strip(),
        })
    except requests.RequestException:
        return False, "Connexion à l'API impossible"

    if r.status_code == 201:
        return True, "Le client a été ajouté avec succès"
    return False, utils.error_message(r)


# ======== Profile client ========

def get_client(client_id: int) -> dict | None:
    try:
        r = requests.get(f"{utils.API}/clients/{client_id}", timeout=5)
    except requests.RequestException:
        return None
    
    if r.status_code != 200:
        return None
    
    return r.json() # client (id, name, firstname)


# ========= Remove client ========

def remove_client(client_id: int) -> tuple[bool, str]:
    try:
        r = requests.delete(f"{utils.API}/clients/{client_id}", timeout=5)
    except requests.RequestException:
        return False, "Connexion à l'API impossible"

    # messages in interface 
    if r.ok:
        return True, f"Client supprimé (Numéro client: {client_id})"
    if r.status_code == 404:
        return False, f"Client introuvable (Numéro client: {client_id} )"

    # detail (API)
    try:
        detail = r.json().get("detail", r.text)
    except ValueError:
        detail = r.text
    return False, f"Erreur {r.status_code} : {detail}"


# ======== List clients =========

def get_clients() -> list | None:
    """Liste des clients ou None si l'API est inaccessible ou en erreur"""
    try:
        r = requests.get(f"{utils.API}/clients", timeout=5)
    except requests.RequestException:
        return None
    return r.json() if r.status_code == 200 else None