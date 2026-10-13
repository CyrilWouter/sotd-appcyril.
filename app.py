import sqlite3

# Verbinding maken met de database van je SOTD app
conn = sqlite3.connect('sotd_database.db')
c = conn.cursor()

# Tabel aanmaken als deze nog niet bestaat
c.execute('''
    CREATE TABLE IF NOT EXISTS parfums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naam TEXT UNIQUE,
        merk TEXT,
        type_geur TEXT,
        image_url TEXT,
        rotatie_dag TEXT
    )
''')

# Jouw complete collectie inclusief foto-URL's
mijn_collectie = [
    # --- TOP 5 ---
    ("Rayhaan Obsidian", "Rayhaan", "Dark / Spicy / Woody / Leather", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Geen (Weekend/Vrij)"),
    ("Kismet Angel", "Maison Alhambra", "Warm / Boozy / Gourmand / Sweet", "https://cdn.fragrancex.com/images/products/parent/medium/81329m.jpg", "Geen (Weekend/Vrij)"),
    ("Shiyaaka Shadow", "Khadlaj", "Dark / Leather & Mineral / Woody", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Vrijdag"),
    ("The Master Perfumer Black Musk N° 12", "The Master Perfumer", "Dark / Musk / Woody", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Woensdag"),
    ("Salvatore Ferragamo Uomo EDT", "Salvatore Ferragamo", "Sweet / Tiramisu / Coffee / Warm", "https://cdn.fragrancex.com/images/products/parent/medium/73822m.jpg", "Geen (Weekend/Vrij)"),

    # --- HONORABLE MENTIONS ---
    ("Nautica Voyage", "Nautica", "Aquatic / Fresh Green", "https://cdn.fragrancex.com/images/products/parent/medium/61195m.jpg", "Dinsdag"),
    ("Lattafa Khamrah", "Lattafa", "Sweet / Gourmand / Warm Spice", "https://cdn.fragrancex.com/images/products/parent/medium/79883m.jpg", "Geen (Weekend/Vrij)"),
    ("Loris Frequence Fresh (E-241)", "Loris", "Fresh / Citrus / Tea (Imagination clone)", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Maandag"),
    ("Loris Vanilla Absolute", "Loris", "Rich Vanilla / Extrait de Parfum", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Geen (Weekend/Vrij)"),

    # --- OVERIGE ROTATIE PARFUMS ---
    ("Varanti Hombre Colten Blue EDT", "Varanti", "Blue Fragrance / Fresh Spice", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Donderdag"),
    ("Territoire – Gold 79 Pour Homme EDP", "Territoire", "Sweet / Warm Spice", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Vrijdag"),
    ("Capace Exclusive – Eluan Hombre Woody Vanilla", "Capace", "Rich Vanilla & Wood", "https://fagron.com.br/wp-content/uploads/2023/10/placeholder-300x400.png", "Vrijdag")
]

# Gegevens invoeren of updaten
for parfum in mijn_collectie:
    c.execute('''
        INSERT INTO parfums (naam, merk, type_geur, image_url, rotatie_dag)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(naam) DO UPDATE SET
            merk=excluded.merk,
            type_geur=excluded.type_geur,
            image_url=excluded.image_url,
            rotatie_dag=excluded.rotatie_dag
    ''', parfum)

conn.commit()
conn.close()

print("🔥 Afbeeldingen en collectie succesvol bijgewerkt Cyril!")
