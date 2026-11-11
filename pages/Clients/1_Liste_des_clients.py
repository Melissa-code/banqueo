import streamlit as st

import services.client_service as client_service

st.write("TEST : cette page est bien chargée")

st.title(":material/group: Liste des clients")

# ---------- btn ajouter un client ----------

st.page_link(
    "pages/Clients/3_Ajouter_un_client.py",
    label="Ajouter un client",
    icon=":material/person_add:",
)

# ---------- Data clients ----------

# clients = client_service.get_clients()

import requests
import utils

st.write("API utilisée :", utils.API)
r = requests.get(f"{utils.API}/clients", timeout=5)
st.write("Statut :", r.status_code)
st.write("Réponse :", r.text)
clients = r.json() if r.status_code == 200 else None

if clients is None :
    st.error("Impossible de récupérer les clients.")
    st.stop()
if not clients:
    st.info("Aucun client enregistré.")
    st.stop()

# ---------- Rechercher ----------

search = st.text_input(
    "Rechercher un client",
    placeholder="Numéro, nom ou prénom",
    icon=":material/search:",
)
q = search.strip().lower()
if q:
    clients = [
        c for c in clients
        if q in f"{c['id']} {c['firstname']} {c['lastname']}".lower()
    ]

st.caption(f"{len(clients)} client(s)")


# ---------- Tableau ----------

st.dataframe(
    clients,
    hide_index=True,
    width="stretch",
    column_order=["id", "lastname", "firstname"],
    column_config={
        "id": st.column_config.NumberColumn("Numéro client", format="%d"),
        "lastname": st.column_config.TextColumn("Nom"),
        "firstname": st.column_config.TextColumn("Prénom"),
    },
)