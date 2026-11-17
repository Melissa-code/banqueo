import streamlit as st

from services import client_service
from services import account_service


client_id : str = st.session_state.get("client_id")
client = client_service.get_client(client_id)

if client is None:
    st.error("Client introuvable ou API indisponible.")
    st.stop()


st.title(":material/person: Fiche client")
st.page_link("pages/Clients/1_Liste_des_clients.py", label="Retour à la liste des clients", icon=":material/arrow_back:")
st.write("") # saut de ligne

with st.container(border=True):
    st.markdown(f"#### {client['firstname']} {client['lastname']}")
    st.caption(f"Numéro client : {client['id']}")


# ---------- Modale confirmation ----------

@st.dialog("Confirmer la suppression")
def confirm_delete(client_id, full_name: str):
    st.warning(
        f"Supprimer **{full_name}** et tous ses comptes ? "
        "Cette action est irréversible."
    )
    c1, c2 = st.columns(2)

    if c1.button("Annuler", width="stretch"):
        st.rerun()

    if c2.button("Supprimer", type="primary", icon=":material/delete:", width="stretch"):
        ok, message = client_service.remove_client(client_id)
        if ok:
            st.session_state["flash"] = message
            st.switch_page("pages/Clients/1_Liste_des_clients.py")
        else:
            st.error(message)  # erreur dans modale

# ---------- Actions ----------

if st.button("Supprimer le client", icon=":material/delete:"):
    confirm_delete(client_id, f"{client['firstname']} {client['lastname']} (numéro client: {client['id']})")

# ---------- Tableau de comptes du client ----------

st.subheader("Comptes")

all_accounts = account_service.get_accounts()
if all_accounts is None:
    st.error("Impossible de récupérer les comptes.")
    st.stop()

# on ne garde que les comptes de ce client
accounts = [a for a in all_accounts if a["client_id"] == client["id"]]

if not accounts:
    st.info("Aucun compte pour le moment.")
    st.stop()

event = st.dataframe(
    accounts,
    key="accounts_table",
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True,
    width="stretch",
    column_order=["account_number", "account_name", "balance"],
    column_config={
        "account_number": st.column_config.TextColumn("N° de compte"),
        "account_name": st.column_config.TextColumn("Nom du compte"),
        "balance": st.column_config.TextColumn("Solde (€)"),
    },
)

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
