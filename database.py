import sqlite3

DB_NAME = "assorti.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agence TEXT,
        nom_fichier TEXT,
        metier TEXT,
        competences TEXT,
        caces TEXT,
        permis TEXT,
        texte TEXT,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS postes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agence TEXT,
        entreprise TEXT,
        poste TEXT,
        competences TEXT,
        caces TEXT,
        permis TEXT,
        texte TEXT,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suivi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agence TEXT,
        candidat TEXT,
        entreprise TEXT,
        poste TEXT,
        statut TEXT,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
