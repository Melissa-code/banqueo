from decimal import Decimal, InvalidOperation

import requests
import streamlit as st

# Set page configuration (à mettre en haut du fichier)
st.set_page_config(
    page_title="Banqueo",
    page_icon="🏦",
    layout="centered",
)

API = "http://127.0.0.1:8001"

st.title("🏦 Banqueo")
tab0, tab1, tab2, tab3 = st.tabs(["Accueil", "Client", "Compte", "Opérations"])


def parse_amount(text: str) -> Decimal | None:
    try:
        # accepte virgule 
        value = Decimal(text.replace(",", ".")) 
    except InvalidOperation:
        return None
    return value if value > 0 else None

# Home tab
with tab0:
    st.subheader("Bienvenue sur Banqueo !")
    st.write("Gérez vos clients et leurs comptes bancaires en quelques clics.")

    st.info("Commencez par créer un client dans l'onglet « Client ».")

# CLient tab 
with tab1:
    st.subheader("Créer un client")
    client_id = st.number_input("ID", min_value=1, step=1, key="cid")
    firstname = st.text_input("Prénom")
    lastname = st.text_input("Nom")
    if st.button("Créer le client"):
        r = requests.post(f"{API}/clients", json={
            "id": int(client_id), "firstname": firstname, "lastname": lastname})
        if r.status_code == 201:
            st.success("Client créé !")
        else:
            st.error(r.json()["detail"])

# Account tab
with tab2:
    st.subheader("Ouvrir un compte")
    cid = st.number_input("ID du client", min_value=1, step=1, key="cid2")
    name = st.text_input("Nom du compte (ex : Livret A)")
    number = st.text_input("Numéro de compte")
    balance = st.text_input("Solde initial", value="0.00")
    if st.button("Ouvrir le compte"):
        value = parse_amount(balance, allow_zero=True)
        if value is None:
            st.error("Solde initial invalide")
        else: 
            r = requests.post(f"{API}/clients/{int(cid)}/accounts", json={
                "account_name": name, "account_number": number,
                "initial_balance": str(value)})
            if r.status_code == 201:
                st.success(f"Compte ouvert, solde : {r.json()['balance']} €")
            else:
                st.error(r.json()["detail"])

# Operations tab
with tab3:
    st.subheader("Dépôt / retrait")
    acc = st.text_input("Numéro de compte", key="acc")
    amount = st.text_input("Montant", value="10.00")
    col1, col2 = st.columns(2)
    if col1.button("Déposer"):
        value = parse_amount(amount)
        if value is None:
            st.error("Montant invalide")
        else: 
            r = requests.post(f"{API}/accounts/{acc}/deposit", json={"amount": str(value)})
            st.success(f"Nouveau solde : {r.json()['balance']} €") if r.ok else st.error(r.json()["detail"])
    if col2.button("Retirer"):
        value = parse_amount(amount)
        if value is None:
            st.error("Montant invalide")
        else:
            r = requests.post(f"{API}/accounts/{acc}/withdraw", json={"amount": str(value)})
            st.success(f"Nouveau solde : {r.json()['balance']} €") if r.ok else st.error(r.json()["detail"])

    if st.button("Voir l'historique"):
        r = requests.get(f"{API}/accounts/{acc}/history")
        if r.ok:
            st.table(r.json())
        else:
            st.error(r.json()["detail"])

