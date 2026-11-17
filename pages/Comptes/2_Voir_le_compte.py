from decimal import Decimal

import streamlit as st

from services import account_service


st.title(":material/account_balance_wallet: Détail du compte")

# message après une opération (dépôt / retrait)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"), icon=":material/check:")

st.page_link("pages/Comptes/1_Liste_des_comptes.py", label="Retour à la liste des comptes", icon=":material/arrow_back:")
st.write("") # saut de ligne

account_number = st.session_state.get("account_number")

if not account_number:
    st.info("Aucun compte sélectionné")
    st.stop()

account = account_service.get_account(account_number)
if account is None:
    st.error("Impossible de récupérer ce compte")
    st.stop()

# ---------- Client titulaire du compte ----------

client_id = account["client_id"] if account["client_id"] is not None else "—"
prenom = account["client_firstname"] or "—"
nom = account["client_lastname"] or "—"

with st.container(border=True):
    st.markdown(f"#### {account['account_name']} n° {account['account_number']}")
    st.markdown(f"**Solde :** {account['balance']} €")
    st.markdown(f"**Client n°** {client_id} : {prenom} {nom}")

# ---------- Suppression ----------

@st.dialog("Confirmer la suppression")
def confirm_delete_account(number: str) -> None:
    st.warning(
        f"Supprimer le compte **{number}** ? Cette action est irréversible."
    )
    c1, c2 = st.columns(2)

    if c1.button("Annuler", width="stretch"):
        st.rerun()

    if c2.button("Supprimer", type="primary", icon=":material/delete:", width="stretch"):
        ok, message = account_service.remove_account(number)
        if ok:
            st.session_state["flash"] = message
            st.switch_page("pages/Comptes/1_Liste_des_comptes.py")
        else:
            st.error(message)  


if st.button("Supprimer le compte", icon=":material/delete:", type="secondary"):
    confirm_delete_account(account["account_number"])

# ---------- Opérations ----------

tab_depot, tab_retrait = st.tabs(["Déposer", "Retirer"])

with tab_depot:
    with st.form("form_depot"):
        montant_depot = st.number_input(
            "Montant (€)", key="montant_depot", min_value=0.01, step=0.01,
            format="%.2f", value=None, placeholder="0.00", required=True,
        )
        if st.form_submit_button("Déposer", type="primary"):
            if montant_depot is None:
                st.error("Saisissez un montant.")
            else:
                ok, message = account_service.deposit(account_number, Decimal(str(montant_depot)))
                if ok:
                    st.session_state["flash"] = message
                    st.rerun()
                else:
                    st.error(message)

with tab_retrait:
    with st.form("form_retrait"):
        montant_retrait = st.number_input(
            "Montant (€)", key="montant_retrait", min_value=0.01, step=0.01,
            format="%.2f", value=None, placeholder="0.00", required=True,
        )
        if st.form_submit_button("Retirer", type="primary"):
            if montant_retrait is None:
                st.error("Saisissez un montant.")
            else:
                ok, message = account_service.withdraw(account_number, Decimal(str(montant_retrait)))
                if ok:
                    st.session_state["flash"] = message
                    st.rerun()
                else:
                    st.error(message)

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
            "type": st.column_config.TextColumn("Opération"),
            "amount": st.column_config.TextColumn("Montant (€)"),
            "balance": st.column_config.TextColumn("Solde après opération (€)"),
        },
    )
