import streamlit as st
import services.client_service as client_service


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

# for account in accounts:
#     with st.container(border=True):
#         c1, c2 = st.columns([3, 1])
#         c1.markdown(f"**{account['account_name']}**")
#         c1.caption(account["account_number"])
#         c2.metric("Solde", f"{account['balance']} €")

# ---------- Actions ----------

col1, col2 = st.columns(2)
col1.button("Modifier le client", icon=":material/edit:", width="stretch")
col2.button("Supprimer le client", icon=":material/delete:", width="stretch")
