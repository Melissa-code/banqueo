import streamlit as st

from services import client_service

client_id : str = st.session_state.get("client_id")
client = client_service.get_client(client_id)


if client is None:
    st.error("Client introuvable ou API indisponible.")
    st.stop()


st.title(f":material/person: {client['firstname']} {client['lastname']}")
st.caption(f"Numéro client : {client['id']}")

st.divider()

# ---------- Comptes ----------

st.subheader("Comptes")
st.info("Aucun compte pour le moment.") 

# TODO accounts
# for account in accounts:
#     with st.container(border=True):
#         c1, c2 = st.columns([3, 1])
#         c1.markdown(f"**{account['account_name']}**")
#         c1.caption(account["account_number"])
#         c2.metric("Solde", f"{account['balance']} €")

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

col1, col2 = st.columns(2)
col1.button("Modifier le client", icon=":material/edit:", width="stretch")

if col2.button("Supprimer le client", icon=":material/delete:", width="stretch"):
    confirm_delete(client_id, f"{client['firstname']} {client['lastname']} (numéro client: {client['id']})")

 
