 import streamlit as st

# Stały domyślny stan magazynu
DOMYSLNY_MAGAZYN = "Laptop (12)\nMonitor (5)\nKlawiatura (20)"

def konwertuj_na_liste(tekst_magazynu):
    """Konwertuje tekst z pola na listę pozycji."""
    # Usuwamy puste linie, a następnie dzielimy tekst na listę
    return [linia.strip() for linia in tekst_magazynu.split('\n') if linia.strip()]

def konwertuj_na_tekst(lista_magazynu):
    """Konwertuje listę pozycji z powrotem na tekst."""
    return '\n'.join(lista_magazynu)

def dodaj_towar(aktualny_tekst, nowy_towar):
    """Dodaje nowy towar i zwraca zaktualizowany tekst."""
    if not nowy_towar:
        st.error("Wprowadź nazwę towaru do dodania.")
        return aktualny_tekst
        
    lista = konwertuj_na_liste(aktualny_tekst)
    
    # Dodanie tylko jeśli towaru nie ma (lub zawsze, zależy od logiki biznesowej)
    if nowy_towar not in lista:
        lista.append(nowy_towar)
        st.success(f"Dodano: {nowy_towar}")
    else:
        st.info(f"Towar '{nowy_towar}' jest już w magazynie.")
        
    return konwertuj_na_tekst(lista)

## --- Interfejs użytkownika Streamlit ---

st.title("🛒 Prosty Magazyn (Bez Session State)")
st.caption("Magazyn jest przechowywany w polu tekstowym i modyfikowany przy interakcji.")

# 1. Pole tekstowe przechowujące aktualny stan magazynu
# Używamy DOMYSLNY_MAGAZYN jako początkowej wartości
aktualny_magazyn_tekst = st.text_area(
    "Aktualny Stan Magazynu (Edytuj bezpośrednio lub użyj formularzy)",
    value=DOMYSLNY_MAGAZYN,
    height=200,
    key="glowny_magazyn_input"
)

# Konwersja na listę dla łatwiejszej manipulacji
lista_magazynu = konwertuj_na_liste(aktualny_magazyn_tekst)

st.divider()

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Nowy Towar")

with st.form(key='dodaj_formularz'):
    nowy_towar = st.text_input("Nazwa Towaru (np. 'Myszka (15)')")
    przycisk_dodaj = st.form_submit_button("Dodaj do Magazynu")

    if przycisk_dodaj:
        # Zaktualizuj i nadpisz wartość w głównym polu tekstowym
        nowy_tekst = dodaj_towar(aktualny_magazyn_tekst, nowy_towar)
        st.session_state.glowny_magazyn_input = nowy_tekst
        st.rerun() # Wymuś odświeżenie po zmianie

st.divider()

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

if lista_magazynu:
    # Tworzymy listę wyboru na podstawie numerów pozycji
    opcje_usuwania = [f"{i+1}. {towar}" for i, towar in enumerate(lista_magazynu)]
    
    # Wybór towaru do usunięcia
    wybrany_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia",
        options=opcje_usuwania,
        index=0
    )
    
    if st.button("Usuń Wybrany Towar"):
        # Pobieramy indeks (numer pozycji - 1)
        indeks_do_usuniecia = opcje_usuwania.index(wybrany_do_usuniecia)
        
        usuniety_towar = lista_magazynu.pop(indeks_do_usuniecia)
        
        # Konwersja z powrotem na tekst
        nowy_tekst = konwertuj_na_tekst(lista_magazynu)
        
        # Nadpisz wartość w głównym polu tekstowym
        st.session_state.glowny_magazyn_input = nowy_tekst
        st.warning(f"Usunięto: {usuniety_towar}")
        st.rerun() # Wymuś odświeżenie
        
else:
    st.info("Magazyn jest pusty, nic do usunięcia.")

st.divider()
st.info("UWAGA: Ten kod działa poprzez nadpisywanie pola `st.text_area` za pomocą `st.session_state` (tylko do kontroli komponentu). Stan magazynu jest fizycznie zapisany w tekście w polu.")
