import requests
import streamlit as st
import utils
import re

API = utils.API

NAME_PATTERN = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$")

NAME_VALIDATE = (
    NAME_PATTERN.pattern,
    "Lettres, espaces, apostrophes et tirets uniquement.",
)

def validate_client(client_id: int, lastname: str, firstname: str) -> str | None:
    """Renvoie un message d'erreur ou None si valide"""
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

