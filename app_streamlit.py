import streamlit as st

st.set_page_config(page_title="Banqueo", page_icon="🏦", layout="centered")

pages = {
    "": [
        st.Page("pages/Accueil.py", title="Accueil", icon=":material/home:", default=True),
    ],
    "Clients": [
        st.Page("pages/Clients/1_Liste_des_clients.py", title="Liste des clients", icon=":material/group:"),
        st.Page("pages/Clients/2_Voir_la_fiche_client.py", title="Fiche client", icon=":material/person:"),
        st.Page("pages/Clients/3_Ajouter_un_client.py", title="Ajouter un client", icon=":material/person_add:"),
    ],
    "Comptes": [
         st.Page("pages/Comptes/4_Operations.py", title="Opérations", icon=":material/payments:"),
    ],
}

pg = st.navigation(pages)
pg.run()