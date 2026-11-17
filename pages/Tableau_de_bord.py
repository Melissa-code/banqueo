from decimal import Decimal

import streamlit as st

from services import account_service, client_service

st.set_page_config(page_title="Banqueo", page_icon=":material/space_dashboard:", layout="wide")

# ---------- En-tête ----------

st.title(":material/space_dashboard: Tableau de bord")
st.caption("Gestion des clients et de leurs comptes bancaires")

st.write("") # saut de ligne

# ---------- Données ----------

clients = client_service.get_clients()
accounts = account_service.get_accounts()

if clients is None or accounts is None:
    st.error("Impossible de joindre l'API Banqueo. Vérifiez qu'elle est lancée.")
    st.stop()

total_solde = sum(Decimal(a["balance"]) for a in accounts)

# ---------- Indicateurs ----------

col1, col2, col3 = st.columns(3)
col1.metric("Clients", len(clients), border=True)
col2.metric("Comptes", len(accounts), border=True)
col3.metric("Solde total", f"{total_solde:,.2f} €".replace(",", " "), border=True)

st.write("") # saut de ligne

# ---------- Actions rapides ----------

st.markdown("##### Actions rapides")
a1, a2, a3, a4 = st.columns(4)
a1.page_link("pages/Clients/3_Ajouter_un_client.py", label="Ajouter un client", icon=":material/person_add:")
a2.page_link("pages/Clients/1_Liste_des_clients.py", label="Liste des clients", icon=":material/group:")
a3.page_link("pages/Comptes/3_Ouvrir_un_compte.py", label="Ouvrir un compte", icon=":material/add_card:")
a4.page_link("pages/Comptes/1_Liste_des_comptes.py", label="Liste des comptes", icon=":material/cards_stack:")

st.divider()

# ---------- Derniers comptes ----------

st.markdown("##### Derniers comptes ouverts")

if not accounts:
    st.info("Aucun compte pour le moment. Commencez par ajouter un client, puis ouvrez-lui un compte.")
else:
    st.dataframe(
        list(reversed(accounts))[:5],
        hide_index=True,
        width="stretch",
        column_order=["account_number", "account_name", "balance", "client_firstname", "client_lastname"],
        column_config={
            "account_number": st.column_config.TextColumn("N° de compte"),
            "account_name": st.column_config.TextColumn("Type"),
            "balance": st.column_config.TextColumn("Solde (€)"),
            "client_firstname": st.column_config.TextColumn("Prénom"),
            "client_lastname": st.column_config.TextColumn("Nom"),
        },
    )
    st.page_link("pages/Comptes/1_Liste_des_comptes.py", label="Voir tous les comptes", icon=":material/arrow_forward:")
