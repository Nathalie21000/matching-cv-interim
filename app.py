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
    st.subheader("Analyse CV - ID'EES INTERIM")

    cv_file = st.file_uploader("Déposez un CV (PDF)", type=["pdf"])
    job_file = st.file_uploader("Déposez une fiche de poste (PDF)", type=["pdf"])

    if cv_file and job_file:
        st.success("Fichiers reçus ✔")

        st.info("Analyse en cours...")

        st.write("### Résultat (version test)")
        st.metric("Compatibilité", "87 %")

        st.write("#### Points forts")
        st.write("- Expérience similaire")
        st.write("- Compétences techniques compatibles")

        st.write("#### Points à vérifier")
        st.write("- Disponibilité à confirmer")

elif menu == "👥 CVthèque (bientôt)":
    st.warning("Module en construction")

elif menu == "📋 Fiches de poste (bientôt)":
    st.warning("Module en construction")

elif menu == "🤝 Matching (bientôt)":
    st.warning("Module en construction")
