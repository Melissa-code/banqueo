import streamlit as st

from services import client_service

client_id : str = st.session_state.get("client_id")

# message (ex success delete client)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"), icon=":material/check:")


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

event = st.dataframe(
    clients,
    key="clients_table",
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True,
    width="stretch",
    column_order=["id", "lastname", "firstname"],
    column_config={
        "id": st.column_config.NumberColumn("Numéro client", format="%d"),
        "lastname": st.column_config.TextColumn("Nom"),
        "firstname": st.column_config.TextColumn("Prénom"),
    },
)

# ---------- Voir la fiche du client sélectionné ----------

selected_rows = event.selection.rows
if selected_rows:
    selected_client = clients[selected_rows[0]]
    st.write("") # saut de ligne
    if st.button(
        f"Voir la fiche client",
        icon=":material/person:",
        type="primary",
    ):
        st.session_state["client_id"] = selected_client["id"]
        st.switch_page("pages/Clients/2_Voir_la_fiche_client.py")
else:
    st.caption("Sélectionnez une ligne du tableau pour voir la fiche client.")