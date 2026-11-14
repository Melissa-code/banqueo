import streamlit as st

from services import account_service

client_id : str = st.session_state.get("client_id")

# message (ex success delete client)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"), icon=":material/check:")


st.title(":material/cards_stack: Liste de tous les comptes clients")
st.write("") # saut de ligne 

# ---------- btn add account----------

st.page_link(
    "pages/Comptes/3_Ouvrir_un_compte.py",
    label="Ouvrir un compte",
    icon=":material/add_card:",
)
st.write("") # saut de ligne 

# ---------- Data accounts ----------

accounts = account_service.get_accounts()

if accounts is None :
    st.error("Impossible de récupérer les comptes clients.")
    st.stop()
if not accounts:
    st.info("Aucun compte enregistré")
    st.write("") # saut de ligne 
    st.stop()

# ---------- Rechercher ----------

search = st.text_input(
    "Rechercher un compte",
    placeholder="Numéro de compte",
    icon=":material/search:",
)
q = search.strip().lower()
if q:
    accounts = [
        c for c in accounts
        if q in f"{c['account_number']}".lower()
    ]

st.caption(f"{len(accounts)} compte(s)")

# ---------- Tableau ----------

st.dataframe(
    accounts,
    hide_index=True,
    width="stretch",
    column_order=["account_number", "account_name", ],
    column_config={
        "account_number": st.column_config.TextColumn("Numéro de compte"),
        "account_name": st.column_config.TextColumn("Nom du compte"),
    },
)