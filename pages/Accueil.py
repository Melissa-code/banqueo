import streamlit as st

st.set_page_config(page_title="Banqueo", page_icon=":material/account_balance:", layout="centered")

# ---------- Accroche ----------

st.title(":material/account_balance: Banqueo")
st.subheader("Vos comptes bancaires, en un seul endroit.")

b1, b2 = st.columns(2)
if b1.button("Se connecter", icon=":material/login:", type="primary", width="stretch"):
    # TODO: page de connexion (authentification FastAPI, à venir)
    st.switch_page("pages/Tableau_de_bord.py")
if b2.button("Créer un compte", icon=":material/person_add:", width="stretch"):
    # TODO: création de compte (à venir avec l'authentification)
    st.switch_page("pages/Clients/3_Ajouter_un_client.py")

st.write("") # saut de ligne

# ---------- Pour qui ----------

st.markdown("#### Pour qui ?")
c1, c2 = st.columns(2)

with c1.container(border=True):
    st.markdown("### :material/badge:")
    st.markdown("**Gestionnaire**")
    st.caption("Gérez l'agence au quotidien")
    st.markdown(
        "- Créer et suivre les clients\n"
        "- Ouvrir les comptes\n"
        "- Effectuer les opérations"
    )

with c2.container(border=True):
    st.markdown("### :material/person:")
    st.markdown("**Client**")
    st.caption("Suivez vos comptes")
    st.markdown(
        "- Voir vos comptes et leur solde\n"
        "- Consulter vos opérations\n"
        "- Accès limité à vos informations"
    )

st.write("") # saut de ligne

# ---------- Fonctionnalités ----------

st.markdown("#### Fonctionnalités")
f1, f2, f3 = st.columns(3)

with f1.container(border=True):
    st.markdown("### :material/group:")
    st.markdown("**Clients**")
    st.caption("Fiches et recherche rapide")

with f2.container(border=True):
    st.markdown("### :material/cards_stack:")
    st.markdown("**Comptes**")
    st.caption("Types et plafonds respectés")

with f3.container(border=True):
    st.markdown("### :material/payments:")
    st.markdown("**Opérations**")
    st.caption("Dépôts, retraits, historique")

st.write("") # saut de ligne
st.caption("Banqueo · application de gestion bancaire")
