import streamlit as st
import pdfplumber
import json
import os

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="ID'EES INTERIM - IA RH", layout="wide")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ----------------------------
# HEADER
# ----------------------------
st.title("ID'EES INTERIM - Assistant IA RH")

# ----------------------------
# SIDEBAR
# ----------------------------
agence = st.sidebar.selectbox(
    "🏢 Agence",
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
        "🟢 Matching CV + Poste",
        "🔵 CV → Postes",
        "🔴 Poste → Candidats",
        "📬 Suivi candidatures"
    ]
)

# ----------------------------
# OUTILS
# ----------------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def score_text(cv_text, job_text):
    cv_words = set(cv_text.split())
    job_words = set(job_text.split())

    if len(job_words) == 0:
        return 0, set()

    common = cv_words.intersection(job_words)
    score = len(common) / len(job_words) * 100
    return score, common

# ----------------------------
# ACCUEIL
# ----------------------------
if menu == "🏠 Accueil":
    st.subheader("Bienvenue dans l'assistant RH ID'EES INTERIM")
    st.write("Outil d’analyse CV et matching simplifié pour les agences.")

# ----------------------------
# 1. MATCHING CV + POSTE
# ----------------------------
elif menu == "🟢 Matching CV + Poste":

    st.subheader("Matching CV / Fiche de poste")

    cv_file = st.file_uploader("CV (PDF)", type=["pdf"])
    job_file = st.file_uploader("Fiche de poste (PDF)", type=["pdf"])

    if cv_file and job_file:
        cv_text = extract_text(cv_file)
        job_text = extract_text(job_file)

        score, common = score_text(cv_text, job_text)

        st.metric("Compatibilité", f"{score:.0f} %")

        if score > 70:
            st.success("🟢 Profil recommandé")
        elif score > 40:
            st.warning("🟡 Profil à étudier")
        else:
            st.error("🔴 Profil peu compatible")

        st.write("Mots clés communs :", list(common)[:20])

# ----------------------------
# 2. CV → POSTES
# ----------------------------
elif menu == "🔵 CV → Postes":

    st.subheader("CV → Postes disponibles")

    cv_file = st.file_uploader("CV (PDF)", type=["pdf"])
    job_file = st.file_uploader("Fiches de poste (PDF ou texte multi)", type=["pdf"])

    if cv_file and job_file:
        cv_text = extract_text(cv_file)
        job_text = extract_text(job_file)

        score, common = score_text(cv_text, job_text)

        st.write("### Analyse du CV")
        st.write("Compétences détectées :", list(set(cv_text.split()))[:20])

        st.write("### Compatibilité globale")
        st.metric("Score global", f"{score:.0f} %")

        st.info("👉 Ce CV peut être proposé sur les missions disponibles")

# ----------------------------
# 3. POSTE → CANDIDATS
# ----------------------------
elif menu == "🔴 Poste → Candidats":

    st.subheader("Poste → candidats compatibles")

    job_file = st.file_uploader("Fiche de poste (PDF)", type=["pdf"])
    cv_file = st.file_uploader("CV candidat (PDF)", type=["pdf"])

    if job_file and cv_file:

        job_text = extract_text(job_file)
        cv_text = extract_text(cv_file)

        score, common = score_text(cv_text, job_text)

        st.metric("Compatibilité candidat", f"{score:.0f} %")

        if score > 70:
            st.success("🟢 Candidat fortement recommandé")
        else:
            st.warning("🟡 Candidat à valider")

# ----------------------------
# 4. SUIVI CANDIDATURES
# ----------------------------
elif menu == "📬 Suivi candidatures":

    st.subheader("Suivi CV envoyé")

    nom = st.text_input("Nom candidat")
    poste = st.text_input("Poste / Mission")

    statut = st.selectbox(
        "Statut",
        ["🟡 En attente", "🟢 Mission", "🔴 Refus"]
    )

    if st.button("Enregistrer suivi"):
        data = {
            "agence": agence,
            "nom": nom,
            "poste": poste,
            "statut": statut
        }

        file_path = f"data/suivi_{agence.replace(' ', '_')}.jsonl"

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

        st.success("Suivi enregistré ✔") 
