import streamlit as st
import pandas as pd

# --- FUNKCJA WSTAWIAJĄCA TŁO STRONY ZA POMOCĄ CSS ---
def ustaw_tlo_strony(obraz_url):
    """
    Ustawia obrazek jako tło całej strony Streamlit za pomocą niestandardowego CSS.
    
    UWAGA: Aby ten kod działał poprawnie, obrazek musi być dostępny pod 
    publicznym adresem URL, np. z GitHub Pages lub zewnętrznego hostingu.
    
    Parametr:
        obraz_url (str): URL obrazka tła.
    """
    # Możesz dostosować wartości 'opacity' (przezroczystość tła) oraz 'background-size'
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({obraz_url});
            background-size: cover; /* Pokrywa cały obszar */
            background-repeat: no-repeat;
            background-attachment: fixed; /* Tło się nie przewija */
            opacity: 0.9; /* Opcjonalnie: Ustawienie lekkiej przezroczystości tła */
        }}
        /* Poprawa czytelności tekstu na tle */
        section[data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.9); /* Jasne tło paska bocznego */
        }}
        div.block-container {{
            background-color: rgba(255, 255, 255, 0.9); /* Lekkie, półprzezroczyste tło głównej sekcji */
            padding-top: 2rem;
            padding-bottom: 2rem;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. Konfiguracja i Inicjalizacja Stanu Magazynu ---

# Ustawienie tła strony (URL do Twojego obrazka tła)
# Zastąp ten URL linkiem do Twojego obrazka!
URL_OBRAZKA_TŁA = "https://images.unsplash.com/photo-1620712943265-f939e8f497a6" 
ustaw_tlo_strony(URL_OBRAZKA_TŁA)

st.set_page_config(
    page_title="Magazyn Estetyczny",
    layout="wide"
)

if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [
        "Laptop (12)", 
        "Monitor (5)", 
        "Klawiatura (20)"
    ]

## --- 2. Funkcje Logiki ---
# (Funkcje dodawania i usuwania towaru pozostają bez zmian)
def dodaj_towar():
    """Dodaje nowy towar do listy w st.session_state."""
    nowy_towar = st.session_state.nowy_towar_input
    
    if nowy_towar:
        st.session_state.magazyn.append(nowy_towar)
        st.success(f"Dodano: {nowy_towar}")
        st.session_state.nowy_towar_input = ""
    else:
        st.error("Wprowadź nazwę towaru.")

def usun_towar():
    """Usuwa wybrany towar z listy w st.session_state."""
    wybrana_opcja = st.session_state.wybrany_do_usuniecia
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(st.session_state.magazyn)]
    
    if wybrana_opcja in opcje_usuwania:
        indeks_do_usuniecia = opcje_usuwania.index(wybrana_opcja)
        usuniety_towar = st.session_state.magazyn.pop(indeks_do_usuniecia)
        st.warning(f"Usunięto: {usuniety_towar}")
    else:
        st.error("Nieprawidłowy wybór do usunięcia.")


## --- 3. Interfejs Użytkownika Streamlit ---

# 🖼️ DODANIE OBRAZKA/LOGO
# Możesz użyć URL lub ścieżki do pliku w Twoim repozytorium (np. "logo.png")
LOGO_URL = "https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/static/logo.png" 
st.image(LOGO_URL, width=100)

st.title("🛒 Magazyn z Zapamiętywaniem Stanu")
st.caption("Stan magazynu jest zachowany dzięki `st.session_state`.")

# Wyświetlanie aktualnego magazynu
st.header("🗃️ Aktualny Stan Magazynu")
if st.session_state.magazyn:
    # Tworzenie DataFrame z listy
    df = pd.DataFrame(st.session_state.magazyn, columns=["Towar"])
    df.index = df.index + 1 # Numerowanie od 1
    st.dataframe(df, use_container_width=True)
else:
    st.info("Magazyn jest pusty.")

st.divider()

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

# Używamy st.form, aby zgrupować pola i przycisk.
with st.form(key='dodaj_formularz'):
    st.text_input("Nazwa Towaru (np. 'Myszka (15)')", key="nowy_towar_input")
    st.form_submit_button("Dodaj do Magazynu", on_click=dodaj_towar)

st.divider()

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

if st.session_state.magazyn:
    # Tworzymy opcje wyboru na podstawie bieżącego stanu magazynu
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(st.session_state.magazyn)]
    
    st.selectbox(
        "Wybierz towar do usunięcia",
        options=opcje_usuwania,
        key="wybrany_do_usuniecia",
        index=0
    )
    
    st.button("Usuń Wybrany Towar", on_click=usun_towar)
        
else:
    st.info("Brak towarów do usunięcia.")

st.divider()
st.success("Magazyn działa poprawnie i zapamiętuje stan!")
