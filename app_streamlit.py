import streamlit as st

st.set_page_config(page_title="Banqueo", page_icon="🏦", layout="centered")

pages = {
    "": [
        st.Page("pages/Accueil.py", title="Accueil", icon=":material/account_balance:", default=True),
        st.Page("pages/Tableau_de_bord.py", title="Tableau de bord", icon=":material/space_dashboard:"),
    ],
    "Clients": [
        st.Page("pages/Clients/1_Liste_des_clients.py", title="Liste des clients", icon=":material/group:"),
        st.Page("pages/Clients/2_Voir_la_fiche_client.py", title="Fiche client", icon=":material/person:"),
        st.Page("pages/Clients/3_Ajouter_un_client.py", title="Ajouter un client", icon=":material/person_add:"),
    ],
    "Comptes": [
        st.Page("pages/Comptes/1_Liste_des_comptes.py", title="Liste des comptes", icon=":material/cards_stack:"),
        st.Page("pages/Comptes/2_Voir_le_compte.py", title="Détail du compte", icon=":material/account_balance_wallet:"),
        st.Page("pages/Comptes/3_Ouvrir_un_compte.py", title="Ouvrir un compte", icon=":material/add_card:"),
    ],
}

pg = st.navigation(pages)
pg.run()