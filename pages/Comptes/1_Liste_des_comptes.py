import streamlit as st

from services import account_service

client_id : str = st.session_state.get("client_id")

# message (ex success delete client)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"), icon=":material/check:")


st.title(":material/cards_stack: Liste des comptes clients")
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

event = st.dataframe(
    accounts,
    key="accounts_table",
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True,
    width="stretch",
    column_order=[
        "account_number", 
        "account_name", 
        "balance",
        "client_id",
        "client_firstname", 
        "client_lastname"
    ],
    column_config={
        "account_number": st.column_config.TextColumn("N° de compte"),
        "account_name": st.column_config.TextColumn("Nom du compte"),
        "balance": st.column_config.TextColumn("Solde (€)"),
        "client_id": st.column_config.NumberColumn("N° client", format="%d"),
        "client_firstname": st.column_config.TextColumn("Prénom"),
        "client_lastname": st.column_config.TextColumn("Nom"),
    },
)

# ---------- Voir le compte sélectionné ----------

selected_rows = event.selection.rows
if selected_rows:
    selected_account = accounts[selected_rows[0]]
    st.write("") # saut de ligne

    if st.button(
        f"Voir le compte n° {selected_account['account_number']}",
        icon=":material/visibility:",
        type="primary",
    ):
        st.session_state["account_number"] = selected_account["account_number"]
        st.switch_page("pages/Comptes/2_Voir_le_compte.py")
else:
    st.caption("Sélectionnez une ligne du tableau pour voir le détail du compte.")