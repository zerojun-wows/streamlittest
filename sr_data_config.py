import streamlit as st

# Dictionaries für die Ordnungswerte
nations_order_dict = {
    "JAPAN": 1,
    "USA": 2,
    "UDSSR": 3,
    "DEUTSCHLAND": 4,
    "GB": 5,
    "FRANKREICH": 6,
    "ITALIEN": 7,
    "PANASIEN": 8,
    "EUROPA": 9,
    "DIE NIEDERLANDE": 10,
    "COMMONWEALTH": 11,
    "PANAMERIKA": 12,
    "SPANIEN": 13,
}

ship_class_order_dict = {
    "U-Boot": 1,
    "Zerstörer": 2,
    "Kreuzer": 3,
    "Schlachtschiff": 4,
    "Flugzeugträger": 5,
}

ship_tier_order_dict = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
}

# Liste der Schiffstypen
ship_type_options = ["standard", "elite", "premium", "spezial"]

# Wichtige Spalten
main_columns = ["Nation", "Typ", "Klasse", "Stufe", "Name"]

# Hilfsspalten
hidden_columns = [
    "Ordnungswert_Nation",
    "Ordnungswert_Klasse",
    "Ordnungswert_Stufe",
]

# Alle Spalten
all_columns = main_columns + hidden_columns


def initialize_session_state() -> None:
    # leere Datenliste für den Ausgangsschiffsbestand
    if "schiffsregister_original" not in st.session_state:
        st.session_state.schiffsregister_original = []

    # leere Datenliste für den Schiffsbestand inklusive Änderungen
    if "schiffsregister_aktuell" not in st.session_state:
        st.session_state.schiffsregister_aktuell = []

    # Initialisieren der Variablen für das Bearbeiten
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None
    if "edit_form_data" not in st.session_state:
        st.session_state.edit_form_data = None
    if "edit_form_result" not in st.session_state:
        st.session_state.edit_form_result = None

    # Flag zur Verhinderung der Mehrfachverarbeitun, Anpassung bei Dateiwechsel
    if "file_processed" not in st.session_state:
        st.session_state.file_processed = False
        st.session_state.last_uploaded_file_hash = None


def clear_session_state():
    # session_state leeren falls nötig
    for key in st.session_state.keys():
        del st.session_state[key]
