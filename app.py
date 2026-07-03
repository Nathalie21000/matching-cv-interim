import streamlit as st
from PyPDF2 import PdfReader

st.title("Matching CV / Fiche de poste - Intérim")

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

cv_file = st.file_uploader("CV (PDF)", type=["pdf"])
job_file = st.file_uploader("Fiche de poste (PDF)", type=["pdf"])

if cv_file and job_file:
    cv_text = extract_text(cv_file)
    job_text = extract_text(job_file)

    cv_words = set(cv_text.split())
    job_words = set(job_text.split())

    if job_words:
        score = len(cv_words & job_words) / len(job_words) * 100

        st.write(f"Compatibilité : {round(score,1)} %")

        if score > 75:
            st.success("Très bon profil")
        elif score > 50:
            st.warning("Profil moyen")
        else:
            st.error("Profil faible")
