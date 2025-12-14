import streamlit as st
import pandas as pd

# DOMYŚLNY STAN MAGAZYNU
# Bez st.session_state, ten stan będzie ładowany przy każdym przerysowaniu.
magazyn = ["Laptop (12)", "Monitor (5)", "Klawiatura (20)"]

# Zmiana tytułu głównego
st.title("🛒 Prosty Magazyn")
st.caption("Stan magazynu jest ładowany od nowa przy każdej akcji (dodawanie/usuwanie) z uwagi na brak st.session_state.")

# Wyświetlanie aktualnego magazynu
st.header("🗃️ Aktualny Stan Magazynu")
if magazyn:
    # Użycie DataFrame do ładniejszego wyświetlania
    df = pd.DataFrame(magazyn, columns=["Towar"])
    df.index = df.index + 1 # Numerowanie od 1
    st.dataframe(df, use_container_width=True)
else:
    st.info("Magazyn jest pusty.")

st.divider()

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

with st.form(key='dodaj_formularz'):
    # Używamy st.form, aby Streamlit przetworzył dane wejściowe
    nowy_towar = st.text_input("Nazwa Towaru (np. 'Myszka (15)')", key="nowy_towar")
    przycisk_dodaj = st.form_submit_button("Dodaj do Magazynu")

    if przycisk_dodaj and nowy_towar:
        # POKAZANIE LOGIKI, KTÓRA JEDNAK ZOSTANIE ANULOWANA PRZEZ RESTART SKRYPTU
        
        # 1. Dodajemy do listy
        magazyn.append(nowy_towar) 
        
        # 2. Wyświetlamy sukces (przed restartem)
        st.success(f"Dodano: {nowy_towar}")
        st.warning("UWAGA: Po ponownym uruchomieniu skryptu (co dzieje się automatycznie w Streamlit po interakcji), dodany towar ZNIKNIE, ponieważ brakuje `st.session_state`.")

st.divider()

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

if magazyn:
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(magazyn)]
    
    # Wybór towaru do usunięcia
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia (wybór z domyślnej listy)",
        options=opcje_usuwania,
        key="wybrany_do_usuniecia"
    )
    
    if st.button("Usuń Wybrany Towar"):
        # POKAZANIE LOGIKI, KTÓRA JEDNAK ZOSTANIE ANULOWANA PRZEZ RESTART SKRYPTU
        
        indeks_do_usuniecia = opcje_usuwania.index(wybrany_do_usuniecia)
        usuniety_towar = magazyn.pop(indeks_do_usuniecia)
        
        st.success(f"Usunięto: {usuniety_towar}")
        st.warning("UWAGA: Po ponownym uruchomieniu skryptu, usunięty towar POWRÓCI, ponieważ brakuje `st.session_state`.")

st.divider()
st.info("W Streamlit, aby stan aplikacji był zachowany po kliknięciu przycisku, **musisz** użyć `st.session_state`.")
