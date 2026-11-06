import requests
import streamlit as st

import utils

API = utils.API

st.title("👤 Clients")

# ---------- READ ----------

st.subheader("Liste des clients")

# ajouter un client 
if st.button("Ajouter un client"):
    st.session_state["add_client"] = True
    st.markdown('<a href="/add_client" target="_self">Ajouter un client</a>', unsafe_allow_html=True)

# rechercher un client 
client_search = st.text_input("Rechercher un client")


r = requests.get(f"{API}/clients")
if r.status_code == 200:
    clients = r.json()
    st.table(clients)
else:
    st.error(utils.error_message(r))
