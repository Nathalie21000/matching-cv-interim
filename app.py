import streamlit as st

st.set_page_config(page_title="ID'EES INTERIM - IA Recrutement", layout="wide")

st.title("ID'EES INTERIM - Assistant IA Recrutement")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Accueil",
        "📄 Analyse CV",
        "👥 CVthèque (bientôt)",
        "📋 Fiches de poste (bientôt)",
        "🤝 Matching (bientôt)"
    ]
)

if menu == "🏠 Accueil":
    st.subheader("Bienvenue dans votre assistant de recrutement")
    st.write("""
    Cet outil va vous permettre de :
    - Analyser des CV automatiquement
    - Comparer un CV à une fiche de poste
    - Construire une CVthèque intelligente
    - Faire du matching candidat / poste
    """)

elif menu == "📄 Analyse CV":
    st.subheader("Analyse CV (version 1)")
    st.info("Prochaine étape : on va brancher l'IA + PDF")

elif menu == "👥 CVthèque (bientôt)":
    st.warning("Module en construction")

elif menu == "📋 Fiches de poste (bientôt)":
    st.warning("Module en construction")

elif menu == "🤝 Matching (bientôt)":
    st.warning("Module en construction")
