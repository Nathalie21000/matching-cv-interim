import streamlit as st
import os
import json

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
st.set_page_config(page_title="ID'EES INTERIM - IA Recrutement", layout="wide")

st.title("ID'EES INTERIM - Assistant IA Recrutement")
agence = st.sidebar.selectbox(
    "🏢 Agence ID'EES INTERIM",
    [
        "ID'EES ALENÇON",
        "ID'EES AVRANCHES",
        "ID'EES DINAN",
        "ID'EES HONFLEUR",
        "ID'EES LE MANS",
        "ID'EES RENNES",
        "ID'EES SAINT-MALO"
    ]
)
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

    import pdfplumber

    cv_file = st.file_uploader("Déposez un CV (PDF)", type=["pdf"])
    job_file = st.file_uploader("Déposez une fiche de poste (PDF)", type=["pdf"])

    if cv_file and job_file:
        st.success("Fichiers reçus ✔")
st.success("Fichiers reçus ✔")
      import json

    cv_data = {
        "agence": agence,
        "cv_name": cv_file.name,
        "job_name": job_file.name
    }

    try:
        with open("data/cv_storage.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(cv_data) + "\n")

        st.info("CV enregistré dans la CVthèque ✔")

    except Exception as e:
        st.error("Erreur sauvegarde CV")
        st.write(str(e))      try:
            with pdfplumber.open(cv_file) as pdf:
                cv_text = "".join(page.extract_text() or "" for page in pdf.pages)

            with pdfplumber.open(job_file) as pdf:
                job_text = "".join(page.extract_text() or "" for page in pdf.pages)

            st.info("Analyse en cours...")

            cv_words = set(cv_text.lower().split())
            job_words = set(job_text.lower().split())

            if len(job_words) == 0:
                st.warning("Fiche de poste vide ou illisible")
            else:
                common_words = cv_words.intersection(job_words)
                score = len(common_words) / len(job_words) * 100

                st.write("### Résultat de compatibilité")
                st.metric("Score", f"{score:.0f} %")

                st.write("### Mots clés communs")
                if len(common_words) > 0:
                    st.write(list(common_words)[:30])
                else:
                    st.write("Aucun mot commun détecté")

        except Exception as e:
            st.error("Erreur lors de la lecture des PDF")
            st.write(str(e))

    


      
