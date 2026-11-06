import requests
import streamlit as st

import utils

API = utils.API

st.title("👤 Client")

# ---------- Get ID ----------

client_id = st.session_state.get("client_id")

if client_id is None:
    st.warning("Aucun client sélectionné. Veuillez revenir à la page précédente pour sélectionner un client.")
    st.page_link("pages/1_Clients.py", label="Retour à la liste des clients")
    st.stop()

# ---------- Profile ----------

st.subheader(f"Profil du client {client_id}")

r = requests.get(f"{API}/clients/{client_id}")
if r.status_code != 200:
    st.error(utils.error_message(r))
    st.stop()

client = r.json()

col1, col2, col3 = st.columns(3)
col1.metric("ID", client["id"])
col2.metric("Prénom", client["firstname"])
col3.metric("Nom", client["lastname"])
