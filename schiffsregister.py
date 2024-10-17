import streamlit as st
import pandas as pd

# Dictionary mit gültigen Nationen und deren Ordnungswerten
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

# Dictionary mit gültigen Schiffstypen und deren Ordnungswerten
ship_type_order_dict = {
    "standard": 1,
    "elite": 2,
    "premium": 3,
    "spezial": 4,
}

# Dictionary mit gültigen Schiffsklassen und deren Ordnungswerten
ship_class_order_dict = {
    "U-Boot": 1,
    "Zerstörer": 2,
    "Kreuzer": 3,
    "Schlachtschiff": 4,
    "Flugzeugträger": 5,
}

# Dictionary mit gültigen Stufen (Tiers) und deren Ordnungswerten
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

# Initialisiere die Schiffsliste (wenn noch keine Daten vorhanden sind)
if "schiffsregister" not in st.session_state:
    st.session_state["schiffsregister"] = []

# Speichere die ursprünglichen Daten
if "original_data" not in st.session_state:
    st.session_state[
        "original_data"
    ] = pd.DataFrame()  # Als leerer DataFrame initialisieren

# Überschrift der App
st.title("Schiffsregister")


# Funktion zum Überprüfen der CSV-Struktur und Validierung der Nationen, Typen, Klassen und Stufen
def check_csv_structure_and_values(df):
    expected_columns = ["Nation", "Typ", "Klasse", "Stufe", "Name"]

    # Überprüfen, ob die Spalten korrekt sind
    if list(df.columns) != expected_columns:
        st.error(
            f"Fehlerhafte CSV-Struktur! Erwartete Spalten: {', '.join(expected_columns)}"
        )
        return False

    # Überprüfen, ob alle Nationen gültig sind
    invalid_nations = df[~df["Nation"].isin(nations_order_dict.keys())]
    if not invalid_nations.empty:
        st.error(
            f"Ungültige Nationen gefunden: {', '.join(invalid_nations['Nation'].unique())}"
        )
        return False

    # Überprüfen, ob alle Typen gültig sind
    invalid_types = df[~df["Typ"].isin(ship_type_order_dict.keys())]
    if not invalid_types.empty:
        st.error(
            f"Ungültige Schiffstypen gefunden: {', '.join(invalid_types['Typ'].unique())}"
        )
        return False

    # Überprüfen, ob alle Klassen gültig sind
    invalid_classes = df[~df["Klasse"].isin(ship_class_order_dict.keys())]
    if not invalid_classes.empty:
        st.error(
            f"Ungültige Schiffsklassen gefunden: {', '.join(invalid_classes['Klasse'].unique())}"
        )
        return False

    # Überprüfen, ob alle Stufen (Tiers) gültig sind
    invalid_tiers = df[~df["Stufe"].isin(ship_tier_order_dict.keys())]
    if not invalid_tiers.empty:
        st.error(
            f"Ungültige Stufen gefunden: {', '.join(invalid_tiers['Stufe'].unique())}"
        )
        return False

    return True


# Funktion zum Hochladen einer CSV-Datei und Berechnung der Ordnungswerte
def upload_csv():
    uploaded_file = st.file_uploader("CSV-Datei hochladen", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Überprüfung der Struktur und der Nationen, Typen, Klassen und Stufen
        if check_csv_structure_and_values(df):
            # Speichere die ursprünglichen Daten
            st.session_state["original_data"] = df.copy()

            # Berechne die Ordnungswerte basierend auf der Nation, dem Typ, der Klasse und der Stufe
            df["Ordnungswert_Nation"] = df["Nation"].apply(
                lambda x: nations_order_dict[x]
            )
            df["Ordnungswert_Typ"] = df["Typ"].apply(
                lambda x: ship_type_order_dict[x]
            )
            df["Ordnungswert_Klasse"] = df["Klasse"].apply(
                lambda x: ship_class_order_dict[x]
            )
            df["Ordnungswert_Stufe"] = df["Stufe"].apply(
                lambda x: ship_tier_order_dict[x]
            )
            st.session_state["schiffsregister"] = df.to_dict("records")
            st.success("Schiffsregister erfolgreich hochgeladen!")
        else:
            st.error("Fehler bei der Validierung der CSV-Datei.")


# Funktion zum Herunterladen des aktuellen Schiffsregisters als CSV
def download_csv():
    df = pd.DataFrame(st.session_state["schiffsregister"])
    return df.to_csv(index=False).encode("utf-8")


# CSV hochladen
st.subheader("Schiffsregister hochladen")
upload_csv()

# Eingabeformular für ein neues Schiff
st.subheader("Neues Schiff hinzufügen")
with st.form(key="new_ship"):
    col1, col2 = st.columns(2)

    with col1:
        nation = st.selectbox("Nation", options=list(nations_order_dict.keys()))
        schiff_typ = st.selectbox(
            "Typ", options=list(ship_type_order_dict.keys())
        )
        klasse = st.selectbox(
            "Klasse", options=list(ship_class_order_dict.keys())
        )

    with col2:
        stufe = st.selectbox("Stufe", options=list(ship_tier_order_dict.keys()))
        name = st.text_input("Name")

    # Berechne die Ordnungswerte basierend auf der Nation, dem Typ, der Klasse und der Stufe
    ordnungswert_nation = nations_order_dict[nation]
    ordnungswert_typ = ship_type_order_dict[schiff_typ]
    ordnungswert_klasse = ship_class_order_dict[klasse]
    ordnungswert_stufe = ship_tier_order_dict[stufe]

    # Einreichungsbutton für das Formular
    submit_button = st.form_submit_button(label="Schiff hinzufügen")

# Wenn das Formular abgeschickt wird, füge den neuen Eintrag zur Liste hinzu
if submit_button:
    new_ship = {
        "Nation": nation,
        "Typ": schiff_typ,
        "Klasse": klasse,
        "Stufe": stufe,
        "Name": name,
        "Ordnungswert_Nation": ordnungswert_nation,
        "Ordnungswert_Typ": ordnungswert_typ,
        "Ordnungswert_Klasse": ordnungswert_klasse,
        "Ordnungswert_Stufe": ordnungswert_stufe,
    }
    st.session_state["schiffsregister"].append(new_ship)
    st.success(f"{name} wurde dem Schiffsregister hinzugefügt!")

# Anzeige des aktuellen Schiffsbestands sortiert nach Ordnungswerten und Namen
if st.session_state["schiffsregister"]:
    st.subheader("Aktueller Schiffsbestand (sortiert)")
    df = pd.DataFrame(st.session_state["schiffsregister"])

    # Sortiere das DataFrame nach den Ordnungswerten und dem Namen
    df.sort_values(
        by=[
            "Ordnungswert_Nation",
            "Ordnungswert_Typ",
            "Ordnungswert_Klasse",
            "Ordnungswert_Stufe",
            "Name",
        ],
        inplace=True,
    )
    st.dataframe(df)

    # Auswahl für das Bearbeiten eines Eintrags über den Schiffsnamen
    ship_names = [ship["Name"] for ship in st.session_state["schiffsregister"]]
    selected_ship_name = st.selectbox(
        "Eintrag zum Bearbeiten auswählen", options=ship_names
    )

    if st.button("Eintrag bearbeiten"):
        # Finde das Schiff, das bearbeitet werden soll
        edit_ship = next(
            ship
            for ship in st.session_state["schiffsregister"]
            if ship["Name"] == selected_ship_name
        )

        with st.form(key="edit_ship"):
            col1, col2 = st.columns(2)

            with col1:
                nation = st.selectbox(
                    "Nation",
                    options=list(nations_order_dict.keys()),
                    index=list(nations_order_dict.keys()).index(
                        edit_ship["Nation"]
                    ),
                )
                schiff_typ = st.selectbox(
                    "Typ",
                    options=list(ship_type_order_dict.keys()),
                    index=list(ship_type_order_dict.keys()).index(
                        edit_ship["Typ"]
                    ),
                )
                klasse = st.selectbox(
                    "Klasse",
                    options=list(ship_class_order_dict.keys()),
                    index=list(ship_class_order_dict.keys()).index(
                        edit_ship["Klasse"]
                    ),
                )

            with col2:
                stufe = st.selectbox(
                    "Stufe",
                    options=list(ship_tier_order_dict.keys()),
                    index=list(ship_tier_order_dict.keys()).index(
                        edit_ship["Stufe"]
                    ),
                )
                name = st.text_input("Name", value=edit_ship["Name"])

            # Berechne die Ordnungswerte
            ordnungswert_nation = nations_order_dict[nation]
            ordnungswert_typ = ship_type_order_dict[schiff_typ]
            ordnungswert_klasse = ship_class_order_dict[klasse]
            ordnungswert_stufe = ship_tier_order_dict[stufe]

            # Einreichungsbutton für das Formular
            submit_edit_button = st.form_submit_button(
                label="Änderungen speichern"
            )

        if submit_edit_button:
            updated_ship = {
                "Nation": nation,
                "Typ": schiff_typ,
                "Klasse": klasse,
                "Stufe": stufe,
                "Name": name,
                "Ordnungswert_Nation": ordnungswert_nation,
                "Ordnungswert_Typ": ordnungswert_typ,
                "Ordnungswert_Klasse": ordnungswert_klasse,
                "Ordnungswert_Stufe": ordnungswert_stufe,
            }
            # Aktualisiere den Eintrag in der Liste
            st.session_state["schiffsregister"] = [
                updated_ship if ship["Name"] == selected_ship_name else ship
                for ship in st.session_state["schiffsregister"]
            ]
            st.success(f"Eintrag '{name}' erfolgreich aktualisiert!")

    # CSV herunterladen
    csv_data = download_csv()
    st.download_button(
        label="Schiffsregister herunterladen",
        data=csv_data,
        file_name="schiffsregister.csv",
        mime="text/csv",
    )

    # Anzeige der Unterschiede zwischen der ursprünglichen und der aktuellen Version
    if not st.session_state[
        "original_data"
    ].empty:  # Überprüfen, ob der DataFrame leer ist
        original_df = st.session_state["original_data"]
        current_df = pd.DataFrame(st.session_state["schiffsregister"])

        # Vergleiche die beiden DataFrames und finde Unterschiede
        differences = current_df.merge(
            original_df,
            on="Name",
            suffixes=("_current", "_original"),
            how="outer",
            indicator=True,
        )
        changes = differences[differences["_merge"] == "both"]

        # Wenn Änderungen vorhanden sind, zeige sie an
        if not changes.empty:
            st.subheader("Änderungen im Vergleich zur Originaldatei")
            for index, row in changes.iterrows():
                changes_summary = f"Änderung im Eintrag '{row['Name']}': "
                for column in ["Nation", "Typ", "Klasse", "Stufe"]:
                    if row[f"{column}_current"] != row[f"{column}_original"]:
                        changes_summary += f"{column} von '{row[f'{column}_original']}' zu '{row[f'{column}_current']}' geändert. "
                st.info(changes_summary)

# Option zum Löschen aller Einträge
if st.button("Alle Einträge löschen"):
    st.session_state["schiffsregister"] = []
    st.session_state[
        "original_data"
    ] = pd.DataFrame()  # Leeren DataFrame zurücksetzen
    st.warning("Alle Einträge wurden gelöscht!")
