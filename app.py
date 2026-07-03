import streamlit as st
import pdfplumber
import json
import os

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="ID'EES INTERIM - IA RH", layout="wide")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

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

def save_jsonl(path, data):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

# ----------------------------
# ACCUEIL
# ----------------------------
if menu == "🏠 Accueil":
    st.subheader("Assistant IA RH simplifié")
    st.write("Analyse CV, fiches de poste et matching pour agences ID'EES.")

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

        if score >= 70:
            st.success("🟢 Profil recommandé")
        elif score >= 40:
            st.warning("🟡 Profil à étudier")
        else:
            st.error("🔴 Profil non adapté")

        st.write("Mots clés :", list(common)[:20])

        # ----------------------------
        # STOCKAGE CV + POSTE
        # ----------------------------
        save_jsonl(
            f"data/cv_{agence.replace(' ', '_')}.jsonl",
            {"text": cv_text[:2000]}
        )

        save_jsonl(
            f"data/poste_{agence.replace(' ', '_')}.jsonl",
            {"text": job_text[:2000]}
        )

# ----------------------------
# 2. CV → POSTES
# ----------------------------
elif menu == "🔵 CV → Postes":

    st.subheader("CV → Postes disponibles")

    cv_file = st.file_uploader("CV (PDF)", type=["pdf"])

    if cv_file:

        cv_text = extract_text(cv_file)

        postes_file = f"data/poste_{agence.replace(' ', '_')}.jsonl"

        if not os.path.exists(postes_file):
            st.warning("Aucune fiche de poste enregistrée pour cette agence")
        else:

            with open(postes_file, "r", encoding="utf-8") as f:
                postes = [json.loads(l)["text"] for l in f.readlines()]

            best_score = 0

            for p in postes:
                score, _ = score_text(cv_text, p)
                best_score = max(best_score, score)

            st.metric("Score global", f"{best_score:.0f} %")

            if best_score >= 70:
                st.success("🟢 CV compatible avec missions disponibles")
            elif best_score >= 40:
                st.warning("🟡 CV partiellement exploitable")
            else:
                st.error("🔴 CV peu exploitable")

# ----------------------------
# 3. POSTE → CANDIDATS
# ----------------------------
elif menu == "🔴 Poste → Candidats":

    st.subheader("Poste → candidats compatibles")

    job_file = st.file_uploader("Fiche de poste (PDF)", type=["pdf"])

    if job_file:

        job_text = extract_text(job_file)

        cv_file_path = f"data/cv_{agence.replace(' ', '_')}.jsonl"

        if not os.path.exists(cv_file_path):
            st.warning("Aucun CV enregistré pour cette agence")
        else:

            with open(cv_file_path, "r", encoding="utf-8") as f:
                cvs = [json.loads(l)["text"] for l in f.readlines()]

            best_score = 0

            for c in cvs:
                score, _ = score_text(c, job_text)
                best_score = max(best_score, score)

            st.metric("Compatibilité candidat", f"{best_score:.0f} %")

            if best_score >= 70:
                st.success("🟢 Candidat recommandé")
            else:
                st.warning("🟡 Aucun candidat idéal, à valider")

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

    if st.button("Enregistrer"):

        save_jsonl(
            f"data/suivi_{agence.replace(' ', '_')}.jsonl",
            {
                "nom": nom,
                "poste": poste,
                "statut": statut
            }
        )

        st.success("Suivi enregistré ✔")
 

  

   
 
