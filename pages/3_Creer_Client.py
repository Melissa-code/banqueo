import requests
import streamlit as st

import utils

API = utils.API

st.title("👤 Client")

# ---------- CREATE ----------

st.subheader("Créer un client")

client_id = st.number_input("ID", min_value=1, step=1, key="cid")
firstname = st.text_input("Prénom", key="new_first")
lastname = st.text_input("Nom", key="new_last")
if st.button("Créer le client"):
    r = requests.post(f"{API}/clients", json={
        "id": int(client_id), "lastname": lastname, "firstname": firstname
    })
    if r.status_code == 201:
        st.success("Client créé !")
        st.rerun()
    else:
        st.error(utils.error_message(r))