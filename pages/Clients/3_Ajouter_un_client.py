import streamlit as st

from services import client_service

st.title(":material/person_add: Ajouter un client")
st.write("") # saut de ligne pour le moment

with st.form("add_client_form", border=True):
    st.markdown("##### Informations du client")

    client_id = st.number_input(
        label="Numéro client", 
        min_value=1, 
        max_value=None,
        key="cid", 
        placeholder="Entrez le numéro du nouveau client", 
        help="Entrez le numéro du nouveau client", 
        required=True, 
        width="stretch", 
    )
    lastname : str = st.text_input(
        label="Nom", 
        key="new_last",
        value="", 
        max_chars=100, 
        placeholder="Entrez le nom du nouveau client", 
        help="Entrez le nom du nouveau client",
        required=True, 
        width="stretch", 
        validate=client_service.NAME_VALIDATE,
    )
    firstname : str = st.text_input(
        label="Prénom", 
        key="new_first",
        value="", 
        max_chars=100, 
        placeholder="Entrez le prénom du nouveau client", 
        help="Entrez le prénom du nouveau client",
        required=True, 
        live=False, 
        width="stretch", 
        validate=client_service.NAME_VALIDATE,
    )

    st.write("")
    submitted = st.form_submit_button("Ajouter le client", type="primary",  width="content", )

    if submitted:
        error = client_service.validate_client(client_id, lastname, firstname)
        if error:
            st.error(error)
        else:
            ok, message = client_service.create_client(client_id, lastname, firstname)
            if ok:
                st.success(message)
                st.session_state["client_id"] = int(client_id)
                st.page_link("pages/Clients/2_Voir_la_fiche_client.py", label="Voir la fiche du client →")
            else:
                st.error(message)