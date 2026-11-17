import streamlit as st

from services import account_service

st.title(":material/account_balance_wallet: Détail du compte")

st.page_link("pages/Comptes/1_Liste_des_comptes.py", label="Retour à la liste des comptes", icon=":material/arrow_back:")
st.write("") # saut de ligne

account_number = st.session_state.get("account_number")

if not account_number:
    st.info("Aucun compte sélectionné.")
    st.stop()

account = account_service.get_account(account_number)
if account is None:
    st.error("Impossible de récupérer ce compte.")
    st.stop()

# ---------- Client titulaire ----------

client_id = account["client_id"] if account["client_id"] is not None else "—"
prenom = account["client_firstname"] or "—"
nom = account["client_lastname"] or "—"

with st.container(border=True):
    st.markdown(f"#### {account['account_name']} n° {account['account_number']}")
    st.markdown(f"**Solde :** {account['balance']} €")
    st.markdown(f"**Client n°** {client_id} : {prenom} {nom}")

# ---------- Historique ----------

st.write("") # saut de ligne
st.markdown("##### Historique des opérations")
history = account_service.get_account_history(account_number)
if history is None:
    st.error("Impossible de récupérer l'historique.")
elif not history:
    st.info("Aucune opération enregistrée.")
else:
    st.dataframe(
        history,
        hide_index=True,
        width="stretch",
        column_order=["date", "type", "amount", "balance"],
        column_config={
            "date": st.column_config.TextColumn("Date"),
            "type": st.column_config.TextColumn("Type"),
            "amount": st.column_config.TextColumn("Montant (€)"),
            "balance": st.column_config.TextColumn("Solde après opération (€)"),
        },
    )
