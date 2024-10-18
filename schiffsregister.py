import pandas as pd
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

ship_type_options = [
    "standard",
    "elite",
    "premium",
    "spezial",
]  # Liste der Schiffstypen


# Hilfsfunktion zum CSV-Download
def download_csv():
    df = pd.DataFrame(st.session_state["schiffsregister"])
    return df.to_csv(index=False).encode("utf-8")


# Lade eine CSV-Datei hoch
uploaded_file = st.file_uploader("Schiffsregister CSV hochladen", type="csv")

# Überprüfe und lade das Schiffsregister
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Überprüfe, ob die erforderlichen Spalten vorhanden sind
    required_columns = ["Nation", "Typ", "Klasse", "Stufe", "Name"]
    if all(column in df.columns for column in required_columns):
        # Ignoriere weitere Spalten und nutze nur die relevanten
        df = df[required_columns]

        # Berechne die Ordnungswerte
        df["Ordnungswert_Nation"] = df["Nation"].map(nations_order_dict)
        df["Ordnungswert_Klasse"] = df["Klasse"].map(ship_class_order_dict)
        df["Ordnungswert_Stufe"] = df["Stufe"].map(ship_tier_order_dict)

        # Initialisiere das Schiffsregister in der Session State
        st.session_state["schiffsregister"] = df.to_dict("records")
        st.session_state["original_data"] = df.copy().to_dict("records")
        st.success("Schiffsregister erfolgreich geladen!")
    else:
        st.error(
            "Die hochgeladene CSV-Datei enthält nicht alle erforderlichen Spalten: Nation, Typ, Klasse, Stufe, Name."
        )

# Wenn kein Schiffsregister existiert, initialisiere eine leere Liste
if "schiffsregister" not in st.session_state:
    st.session_state["schiffsregister"] = []

# Formular zum Hinzufügen eines neuen Schiffs
st.subheader("Neues Schiff hinzufügen")
with st.form(key="new_ship"):
    col1, col2 = st.columns(2)

    with col1:
        new_nation = st.selectbox(
            "Nation", options=list(nations_order_dict.keys())
        )
        new_typ = st.selectbox("Typ", options=ship_type_options)

    with col2:
        new_klasse = st.selectbox(
            "Klasse", options=list(ship_class_order_dict.keys())
        )
        new_stufe = st.selectbox(
            "Stufe", options=list(ship_tier_order_dict.keys())
        )
        new_name = st.text_input("Name")

    submit_new_ship_button = st.form_submit_button(
        label="Neues Schiff hinzufügen"
    )

if submit_new_ship_button:
    # Berechne die Ordnungswerte für das neue Schiff
    new_ordnungswert_nation = nations_order_dict[new_nation]
    new_ordnungswert_klasse = ship_class_order_dict[new_klasse]
    new_ordnungswert_stufe = ship_tier_order_dict[new_stufe]

    new_ship = {
        "Nation": new_nation,
        "Typ": new_typ,
        "Klasse": new_klasse,
        "Stufe": new_stufe,
        "Name": new_name,
        "Ordnungswert_Nation": new_ordnungswert_nation,
        "Ordnungswert_Klasse": new_ordnungswert_klasse,
        "Ordnungswert_Stufe": new_ordnungswert_stufe,
    }

    # Füge das neue Schiff dem Register hinzu
    st.session_state["schiffsregister"].append(new_ship)
    st.success(f"Neues Schiff '{new_name}' erfolgreich hinzugefügt!")

# Anzeige des aktuellen Schiffsbestands sortiert nach Ordnungswerten und Namen
if st.session_state["schiffsregister"]:
    st.subheader("Aktueller Schiffsbestand (sortiert)")
    df = pd.DataFrame(st.session_state["schiffsregister"])

    # Sortiere das DataFrame nach den neuen Ordnungswerten und Namen
    df.sort_values(
        by=[
            "Ordnungswert_Nation",
            "Ordnungswert_Stufe",
            "Ordnungswert_Klasse",
            "Name",
        ],
        inplace=True,
    )
    schiffsbestand_placeholder = st.empty()  # Platzhalter für DataFrame
    schiffsbestand_placeholder.dataframe(df)  # Initiale Anzeige des DataFrames

    # Auswahl für das Bearbeiten eines Eintrags über den Schiffsnamen
    ship_names = [ship["Name"] for ship in st.session_state["schiffsregister"]]
    selected_ship_name = st.selectbox(
        "Eintrag zum Bearbeiten auswählen", options=ship_names
    )

    if selected_ship_name:
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
                typ = st.selectbox(
                    "Typ",
                    options=ship_type_options,
                    index=ship_type_options.index(edit_ship["Typ"]),
                )

            with col2:
                klasse = st.selectbox(
                    "Klasse",
                    options=list(ship_class_order_dict.keys()),
                    index=list(ship_class_order_dict.keys()).index(
                        edit_ship["Klasse"]
                    ),
                )
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
            ordnungswert_klasse = ship_class_order_dict[klasse]
            ordnungswert_stufe = ship_tier_order_dict[stufe]

            # Einreichungsbutton für das Formular
            submit_edit_button = st.form_submit_button(
                label="Änderungen speichern"
            )

        if submit_edit_button:
            updated_ship = {
                "Nation": nation,
                "Typ": typ,
                "Klasse": klasse,
                "Stufe": stufe,
                "Name": name,
                "Ordnungswert_Nation": ordnungswert_nation,
                "Ordnungswert_Klasse": ordnungswert_klasse,
                "Ordnungswert_Stufe": ordnungswert_stufe,
            }
            # Aktualisiere den Eintrag in der Liste
            st.session_state["schiffsregister"] = [
                updated_ship if ship["Name"] == selected_ship_name else ship
                for ship in st.session_state["schiffsregister"]
            ]
            st.success(f"Eintrag '{name}' erfolgreich aktualisiert!")

            # Nach der Bearbeitung, zeige das aktualisierte DataFrame an
            df = pd.DataFrame(st.session_state["schiffsregister"])
            df.sort_values(
                by=[
                    "Ordnungswert_Nation",
                    "Ordnungswert_Stufe",
                    "Ordnungswert_Klasse",
                    "Name",
                ],
                inplace=True,
            )
            schiffsbestand_placeholder.dataframe(
                df
            )  # Aktualisierte Anzeige des DataFrames

    # Löschfunktion
    st.subheader("Eintrag löschen")
    selected_ship_to_delete = st.selectbox(
        "Eintrag zum Löschen auswählen", options=ship_names
    )
    delete_button = st.button("Eintrag löschen")

    if delete_button:
        confirmation = st.text_input(
            f"Bitte bestätigen Sie die Löschung von '{selected_ship_to_delete}'. Geben Sie 'löschen' ein:"
        )
        if confirmation.lower() == "löschen":
            st.session_state["schiffsregister"] = [
                ship
                for ship in st.session_state["schiffsregister"]
                if ship["Name"] != selected_ship_to_delete
            ]
            st.success(
                f"Eintrag '{selected_ship_to_delete}' erfolgreich gelöscht!"
            )
        else:
            st.warning("Löschung abgebrochen.")

# CSV herunterladen
csv_data = download_csv()
st.download_button(
    label="Schiffsregister herunterladen",
    data=csv_data,
    file_name="schiffsregister.csv",
    mime="text/csv",
)
