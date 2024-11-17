import streamlit as st
import pandas as pd
import hashlib
from sr_data_config import (
    nations_order_dict,
    ship_class_order_dict,
    ship_tier_order_dict,
    ship_type_options,
    main_columns,
    hidden_columns,
    all_columns,
    initialize_session_state,
    clear_session_state,
)
from sr_findings import (
    find_new_entries,
    find_modified_entries,
    find_deleted_entries,
)


# Funktion zum Zurücksetzen des Schiffsregisters
def reset_ship_register():
    clear_session_state()
    initialize_session_state()  # Zurücksetzen des session_state
    st.session_state.file_processed = (
        False  # Flag für Dateiverarbeitung zurücksetzen
    )
    st.success("Schiffsregister wurde zurückgesetzt!")


# Funktion zum Hochladen der Datei
def upload_file():
    uploaded_file = st.file_uploader(
        "Wählen Sie eine CSV-Datei zum Hochladen", type="csv"
    )
    if uploaded_file is not None:
        # Berechnung des Hashs der hochgeladenen Datei
        file_hash = hashlib.sha256(uploaded_file.read()).hexdigest()

        # Überprüfen, ob die Datei bereits hochgeladen wurde
        if file_hash != st.session_state.last_uploaded_file_hash:
            # Datei erneut hochladen und in das Schiffsregister laden
            uploaded_file.seek(
                0
            )  # Zurück zum Anfang der Datei, um sie erneut zu lesen
            df = pd.read_csv(uploaded_file)

            # Überprüfen, ob alle main_columns in der Datei vorhanden sind
            missing_columns = [
                col for col in main_columns if col not in df.columns
            ]
            extra_columns = [
                col for col in df.columns if col not in main_columns
            ]

            if missing_columns:
                st.error(f"Fehlende Spalten: {', '.join(missing_columns)}")
            if extra_columns:
                st.warning(f"Zusätzliche Spalten: {', '.join(extra_columns)}")

            # Wenn keine Fehler vorhanden sind, speichern wir die Datei
            if not missing_columns and not extra_columns:
                st.session_state.schiffsregister_aktuell = df.to_dict(
                    orient="records"
                )
                st.session_state.schiffsregister_original = df.to_dict(
                    orient="records"
                )
                st.session_state.last_uploaded_file_hash = file_hash
                st.success("Schiffsregister erfolgreich geladen!")
            else:
                st.warning(
                    "Die Datei wurde aufgrund von Spaltenproblemen nicht hochgeladen."
                )
        else:
            st.info("Dieses Schiffsregister ist bereits geladen.")


def display_ship_register():
    """
    Funktion zur Anzeige des aktuellen Schiffsbestands.
    Überprüft, ob Daten im session_state vorhanden sind und zeigt diese an.
    """
    if (
        "register_updated" in st.session_state
        and st.session_state.register_updated
    ):
        # Anzeigen aktualisieren (Query-Parameter als "weicher" Refresh)
        st.experimental_set_query_params(update="true")
        del st.session_state["register_updated"]

    if (
        "schiffsregister_aktuell" in st.session_state
        and st.session_state.schiffsregister_aktuell
    ):
        # DataFrame aus session_state
        aktuell_df = pd.DataFrame(
            st.session_state.schiffsregister_aktuell, columns=all_columns
        )

        # Anzeige des Schiffsbestands
        st.dataframe(aktuell_df)  # Anzeige des DataFrames
    else:
        st.warning("Kein Schiffsbestand vorhanden!")


def display_new_entries():
    """
    Funktion zur Anzeige der neuen Datensätze im Schiffsregister.
    """
    find_new_entries()
    st.subheader("Zugänge")
    if "added_df" in st.session_state and not st.session_state.added_df.empty:
        st.dataframe(st.session_state.added_df)
    else:
        st.info("Keine Zugänge vorhanden.")


def display_modified_entries():
    """
    Zeigt die geänderten Datensätze an.
    """
    find_modified_entries()
    st.subheader("Veränderungen")
    if (
        "changes_df" in st.session_state
        and not st.session_state.changes_df.empty
    ):
        st.dataframe(st.session_state.changes_df)
    else:
        st.info("Keine Veränderungen vorhanden.")


def display_deleted_entries():
    """
    Zeigt die gelöschten Datensätze an.
    """
    find_deleted_entries()
    st.subheader("Abgänge")
    if (
        "deleted_df" in st.session_state
        and not st.session_state.deleted_df.empty
    ):
        st.dataframe(st.session_state.deleted_df)
    else:
        st.info("Keine Abgänge vorhanden.")


def add_new_ship_form():
    """
    Zeigt ein Formular an, mit dem ein neues Schiff eingetragen werden kann.
    """
    st.subheader("Neues Schiff eintragen")

    with st.form("new_ship_form"):
        col1, col2 = st.columns(2)

        with col1:
            nation = st.selectbox(
                "Nation",
                options=nations_order_dict.keys(),
                key="new_ship_nation",
            )
            typ = st.selectbox(
                "Typ", options=ship_type_options, key="new_ship_type"
            )
            klasse = st.selectbox(
                "Klasse",
                options=ship_class_order_dict.keys(),
                key="new_ship_class",
            )

        with col2:
            stufe = st.selectbox(
                "Stufe",
                options=ship_tier_order_dict.keys(),
                key="new_ship_tier",
            )
            name = st.text_input("Name", key="new_ship_name").strip()

        # Submit-Button des Formulars
        submitted = st.form_submit_button("Schiff hinzufügen")

        # Formular abschließen und Eintrag hinzufügen
        if submitted:
            if name:  # Überprüfen, ob der Name nicht leer ist
                new_ship = {
                    "Nation": nation,
                    "Typ": typ,
                    "Klasse": klasse,
                    "Stufe": stufe,
                    "Name": name,
                }

                # Hinzufügen zum aktuellen Schiffsregister
                st.session_state.schiffsregister_aktuell.append(new_ship)

                st.session_state["register_updated"] = True

                st.success(
                    f"Das Schiff '{name}' wurde erfolgreich hinzugefügt!"
                )
            else:
                st.error("Der Name des Schiffs darf nicht leer sein!")


initialize_session_state()

st.title("Schiffsregisteranwendung")

if st.button("Schiffsregister zurücksetzen"):
    reset_ship_register()

upload_file()

st.header("Aktueller Bestand an Schiffen")

display_ship_register()

display_new_entries()
display_modified_entries()
display_deleted_entries()

st.header("Registerbearbeitung")

add_new_ship_form()

st.write(st.session_state)
