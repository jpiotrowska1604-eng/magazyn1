import streamlit as st
import pandas as pd

## --- 1. Inicjalizacja Stanu Magazynu ---
# Streamlit automatycznie przechowuje dane w st.session_state.
# Sprawdzamy, czy klucz 'magazyn' już istnieje.
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [
        "Laptop (12)", 
        "Monitor (5)", 
        "Klawiatura (20)"
    ]

## --- 2. Funkcje Logiki ---

def dodaj_towar():
    """Dodaje nowy towar do listy w st.session_state."""
    # Pobieramy wartość z pola tekstowego, które ma klucz 'nowy_towar_input'
    nowy_towar = st.session_state.nowy_towar_input
    
    if nowy_towar:
        st.session_state.magazyn.append(nowy_towar)
        st.success(f"Dodano: {nowy_towar}")
        # Opcjonalnie: czyścimy pole wejściowe po dodaniu
        st.session_state.nowy_towar_input = ""
    else:
        st.error("Wprowadź nazwę towaru.")

def usun_towar():
    """Usuwa wybrany towar z listy w st.session_state."""
    # Pobieramy indeks (numer pozycji - 1) z pola selectbox, które ma klucz 'wybrany_do_usuniecia'
    
    # st.session_state.wybrany_do_usuniecia zawiera string np. "1. Laptop (12)".
    # Musimy wydobyć indeks.
    wybrana_opcja = st.session_state.wybrany_do_usuniecia
    
    # Lista wszystkich opcji (do znalezienia indeksu)
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(st.session_state.magazyn)]
    
    if wybrana_opcja in opcje_usuwania:
        indeks_do_usuniecia = opcje_usuwania.index(wybrana_opcja)
        
        # Usuwamy element z listy głównej
        usuniety_towar = st.session_state.magazyn.pop(indeks_do_usuniecia)
        st.warning(f"Usunięto: {usuniety_towar}")
    else:
        st.error("Nieprawidłowy wybór do usunięcia.")

## --- 3. Interfejs Użytkownika Streamlit ---

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
# on_submit kieruje do funkcji dodaj_towar
with st.form(key='dodaj_formularz'):
    # Dodajemy klucz (key) do pola wejściowego, aby móc pobrać jego wartość w funkcji dodaj_towar
    st.text_input("Nazwa Towaru (np. 'Myszka (15)')", key="nowy_towar_input")
    
    # Przycisk, który wywoła funkcję dodaj_towar() po kliknięciu
    st.form_submit_button("Dodaj do Magazynu", on_click=dodaj_towar)

st.divider()

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

if st.session_state.magazyn:
    # Tworzymy opcje wyboru na podstawie bieżącego stanu magazynu
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(st.session_state.magazyn)]
    
    # selectbox zachowuje swój stan w st.session_state.wybrany_do_usuniecia
    st.selectbox(
        "Wybierz towar do usunięcia",
        options=opcje_usuwania,
        key="wybrany_do_usuniecia",
        index=0
    )
    
    # Przycisk, który wywoła funkcję usun_towar() po kliknięciu
    # Nie używamy tu st.form, aby uniknąć konieczności podwójnego submitowania
    st.button("Usuń Wybrany Towar", on_click=usun_towar)
        
else:
    st.info("Brak towarów do usunięcia.")

st.divider()
st.success("Magazyn działa poprawnie i zapamiętuje stan!")
