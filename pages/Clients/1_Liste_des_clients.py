import streamlit as st

from services import client_service

st.title(":material/group: Liste des clients")
st.write("") # saut de ligne pour le moment

# ---------- btn ajouter un client ----------

st.page_link(
    "pages/Clients/3_Ajouter_un_client.py",
    label="Ajouter un client",
    icon=":material/person_add:",
)
st.write("") # saut de ligne pour le moment

# ---------- Data clients ----------

clients = client_service.get_clients()

if clients is None :
    st.error("Impossible de récupérer les clients.")
    st.stop()
if not clients:
    st.info("Aucun client enregistré.")
    st.write("") # saut de ligne pour le moment
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