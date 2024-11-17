import streamlit as st
import pandas as pd

# Beispiel-Daten initialisieren
if "schiffsregister" not in st.session_state:
    st.session_state.schiffsregister = [
        {
            "ID": 1,
            "Name": "Schiff A",
            "Typ": "Kreuzer",
            "Nation": "Deutschland",
        },
        {
            "ID": 2,
            "Name": "Schiff B",
            "Typ": "Schlachtschiff",
            "Nation": "Japan",
        },
        {"ID": 3, "Name": "Schiff C", "Typ": "Zerstörer", "Nation": "USA"},
    ]

# Originaldaten speichern
if "original_data" not in st.session_state:
    st.session_state.original_data = pd.DataFrame(
        st.session_state.schiffsregister
    ).copy()


# Funktion zum Zurücksetzen des DataFrames im Editor
def reset_editor_data():
    st.session_state.schiffsregister = st.session_state.original_data.to_dict(
        "records"
    )
    if "editor" in st.session_state:
        del st.session_state[
            "editor"
        ]  # Entferne Editor-State, um eine vollständige Aktualisierung zu erzwingen


# Buttons für Verwerfungen von Änderungen
if st.button("Alle Änderungen verwerfen"):
    reset_editor_data()

# DataFrame für den Editor aktualisieren
df = pd.DataFrame(st.session_state.schiffsregister)

# Editor neu anzeigen, um Änderungen zu reflektieren
edited_df = st.data_editor(
    df, key="editor", num_rows="dynamic", use_container_width=True
)

# Zeige den aktuellen DataFrame-Stand nach Änderungen an
st.write("Aktueller DataFrame:")
st.write(pd.DataFrame(st.session_state.schiffsregister))
