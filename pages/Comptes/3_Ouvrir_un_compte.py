import streamlit as st

from services import account_service, client_service
from decimal import Decimal


st.title(":material/add_card: Ouvrir un compte client")
st.write("") # saut de ligne 

with st.form("add_account_form", border=True):
    st.markdown("##### Informations du compte")

    # choix du client 
    clients = client_service.get_clients()
    if clients is None:
        st.error("Impossible de charger la liste des clients (API indisponible)")
        st.stop()
    if not clients:
        st.info("Aucun client enregistré. Créez d'abord un client.")
        st.stop()

    client_ids = [c["id"] for c in clients]
    preselected = st.session_state.get("client_id")
    client_index = client_ids.index(int(preselected)) if preselected and int(preselected) in client_ids else None
    client_id = st.selectbox(
        label="Client",
        options=client_ids,
        index=client_index,
        format_func=lambda cid: next(
            f"{c['firstname']} {c['lastname']} - N° client: {cid})" for c in clients if c["id"] == cid
        ),
        key="client_select",
        placeholder="Choisissez un client",
        width="stretch",
    )

    types = account_service.get_account_types()
    if not types:
        st.error("Impossible de charger les types de compte (API indisponible).")
        st.stop()

    # inputs 
    account_name = st.selectbox(
        label="Type de compte",
        options=list(types),          
        key="name_account",
        index=None,  #pas preselect
        placeholder="Choisissez un type de compte",
        help="Le plafond dépend du type de compte choisi",
        width="stretch",
    )
    account_number : str = st.text_input(
        label="Numéro de compte", 
        key="number_account",
        value="", 
        max_chars=20, 
        placeholder="Entrez le numéro du compte", 
        help="Entrez le numéro du compte bancaire",
        required=True, 
        width="stretch", 
        validate=account_service.NAME_ACCOUNT_VALIDATE,
    )
    initial_balance: Decimal = st.number_input(
        label="Solde initial (€)", 
        key="initial_balance_account",
        value=None, 
        min_value=0.0, 
        step=0.01,
        format="%.2f",
        max_value=None,
        placeholder="0.00", 
        help="Entrez le sole initial", 
        required=True, 
        width="stretch", 
    )
    

    st.write("") # saut de ligne 
    submitted = st.form_submit_button("Ouvrir le compte", type="primary",  width="content", )

    if submitted:
        account_number = account_number.strip().upper()
        error = account_service.validate_account(client_id, account_name, account_number)
        if error:
            st.error(error)
        else:
            ok, message = account_service.create_account(
                client_id=client_id,
                account_name=account_name,
                account_number=account_number,
                initial_balance=Decimal(str(initial_balance))
            )
            if ok:
                st.success(message)
                st.session_state["client_id"] = client_id
                # st.page_link("pages/Comptes/2_Voir_le_compte.py", label="Voir le compte du client →")
            else:
                st.error(message)