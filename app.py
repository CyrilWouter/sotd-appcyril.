import datetime
import random
import sqlite3
import streamlit as st

# 1. DATABASE INSTELLINGEN
conn = sqlite3.connect('sotd_database.db', check_same_thread=False)
c = conn.cursor()

# Tabel voor Wear History
c.execute('''
    CREATE TABLE IF NOT EXISTS wear_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum TEXT,
        geurnaam TEXT,
        type_geur TEXT
    )
''')

# Tabel voor Parfum Collectie
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
conn.commit()

# Standaard parfums toevoegen als de database leeg is
c.execute("SELECT COUNT(*) FROM parfums")
if c.fetchone()[0] == 0:
    begin_collectie = [
        ("Loris Frequence Fresh", "Loris", "Fresh / Citrus / Tea", "https://via.placeholder.com/300x400.png?text=Loris+Fresh", "Maandag"),
        ("Nautica Voyage", "Nautica", "Aquatic / Fresh Green", "https://via.placeholder.com/300x400.png?text=Nautica+Voyage", "Dinsdag"),
        ("The Master Perfumer Black Musk N° 12", "Master Perfumer", "Dark / Musk / Woody", "https://via.placeholder.com/300x400.png?text=Black+Musk+N12", "Woensdag"),
        ("Varanti Hombre Colten Blue EDT", "Varanti", "Blue Fragrance / Fresh Spice", "https://via.placeholder.com/300x400.png?text=Colten+Blue", "Donderdag"),
        ("Territoire – Gold 79 Pour Homme EDP", "Territoire", "Sweet / Warm Spice", "https://via.placeholder.com/300x400.png?text=Gold+79", "Vrijdag"),
        ("Shiyaaka Shadow", "Khadlaj", "Dark / Leather & Mineral", "https://via.placeholder.com/300x400.png?text=Shiyaaka+Shadow", "Vrijdag"),
        ("Capace Exclusive – Eluan Hombre Woody Vanilla", "Capace", "Rich Vanilla & Wood", "https://via.placeholder.com/300x400.png?text=Woody+Vanilla", "Vrijdag")
    ]
    c.executemany("INSERT INTO parfums (naam, merk, type_geur, image_url, rotatie_dag) VALUES (?, ?, ?, ?, ?)", begin_collectie)
    conn.commit()

# Pagina Configuratie
st.set_page_config(page_title="SOTD - Cyril", page_icon="🧪", layout="centered")
st.title("🧪 Scent Of The Day (SOTD)")

# TABS NAVIGATIE
tab1, tab2, tab3 = st.tabs(["🎯 SOTD Vandaag", "➕ Collectie Beheer", "📊 Historie"])

# --- TAB 1: SOTD VANDAAG ---
with tab1:
    dagen = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
    vandaag_index = datetime.datetime.now().weekday()
    vandaag_naam = dagen[vandaag_index]
    vandaag_datum = datetime.date.today().strftime("%Y-%m-%d")

    st.write(f"### Vandaag: **{vandaag_naam} ({vandaag_datum})**")

    geur_info = None

    if vandaag_index < 4: # Maandag t/m Donderdag
        c.execute("SELECT naam, merk, type_geur, image_url FROM parfums WHERE rotatie_dag = ?", (vandaag_naam,))
        geur_info = c.fetchone()
    elif vandaag_index == 4: # Vrijdag
        st.warning("🔥 **Casual Friday Special!**")
        c.execute("SELECT naam, merk, type_geur, image_url FROM parfums WHERE rotatie_dag = 'Vrijdag'")
        vrijdag_opties = c.fetchall()
        
        if vrijdag_opties:
            if 'friday_choice' not in st.session_state:
                st.session_state.friday_choice = random.choice(vrijdag_opties)
            
            geur_info = st.session_state.friday_choice
            
            if st.button("🎲 Shuffle Vrijdaggeur"):
                st.session_state.friday_choice = random.choice(vrijdag_opties)
                st.rerun()
    else:
        st.info("😎 **Weekend!** Kies lekker vrij uit je garderobe.")

    if geur_info:
        naam, merk, type_geur, img_url = geur_info
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(img_url if img_url else "https://via.placeholder.com/300x400.png?text=Geen+Foto", caption=naam, use_column_width=True)
        with col2:
            st.success(f"**SOTD:** {naam}")
            st.caption(f"Merk: {merk}")
            st.info(f"**Profiel:** {type_geur}")
            
            if st.button("✅ Bevestig Wear van Vandaag"):
                c.execute("INSERT INTO wear_history (datum, geurnaam, type_geur) VALUES (?, ?, ?)", (vandaag_datum, naam, type_geur))
                conn.commit()
                st.balloons()
                st.toast(f"{naam} gelogd in je historie!", icon="🔥")

# --- TAB 2: COLLECTIE BEHEER (NIEUW PARFUM TOEVOEGEN) ---
with tab2:
    st.subheader("➕ Nieuw Parfum Toevoegen")
    
    with st.form("add_parfum_form", clear_on_submit=True):
        nieuwe_naam = st.text_input("Naam Parfum (bijv. Rayhaan Obsidian)")
        nieuw_merk = st.text_input("Merk / Huis (bijv. Rayhaan)")
        nieuw_type = st.text_input("Geurprofiel (bijv. Dark / Woody / Spicy)")
        nieuwe_foto = st.text_input("Afbeelding URL (optioneel)")
        rotatie = st.selectbox("Rotatie Rol", ["Geen (Weekend/Vrij)", "Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"])
        
        ingediend = st.form_submit_button("💾 Opslaan in Collectie")
        
        if ingediend and nieuwe_naam:
            try:
                c.execute("INSERT INTO parfums (naam, merk, type_geur, image_url, rotatie_dag) VALUES (?, ?, ?, ?, ?)",
                          (nieuwe_naam, nieuw_merk, nieuw_type, nieuwe_foto, rotatie))
                conn.commit()
                st.success(f"🎉 **{nieuwe_naam}** succesvol toegevoegd aan je collectie!")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Deze geurnaam staat al in je database!")

    st.divider()
    st.subheader("📦 Huidige Collectie")
    c.execute("SELECT id, naam, merk, type_geur, rotatie_dag FROM parfums ORDER BY naam ASC")
    alle_parfums = c.fetchall()
    
    for item in alle_parfums:
        p_id, p_naam, p_merk, p_type, p_rotatie = item
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.write(f"• **{p_naam}** ({p_merk}) - *{p_type}* [{p_rotatie}]")
        with col_b:
            if st.button("❌ Wis", key=f"del_{p_id}"):
                c.execute("DELETE FROM parfums WHERE id = ?", (p_id,))
                conn.commit()
                st.rerun()

# --- TAB 3: HISTORIE ---
with tab3:
    st.subheader("📊 Wear History & Statistieken")
    c.execute("SELECT datum, geurnaam, type_geur FROM wear_history ORDER BY id DESC")
    history_data = c.fetchall()
    
    if history_data:
        st.dataframe(history_data, column_config={"0": "Datum", "1": "Parfum", "2": "Type"}, use_container_width=True)
    else:
        st.info("Nog geen logs aanwezig.")
