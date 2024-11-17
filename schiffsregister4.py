import pandas as pd
import streamlit as st
import time
import hashlib

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

#
# ==================== Funktionsbereich ====================
#


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


def calculate_order_values(df) -> None:
    df["Ordnungswert_Nation"] = df["Nation"].map(nations_order_dict)
    df["Ordnungswert_Klasse"] = df["Klasse"].map(ship_class_order_dict)
    df["Ordnungswert_Stufe"] = df["Stufe"].map(ship_tier_order_dict)


def sort_dataframe(df) -> None:
    df.sort_values(
        by=[
            "Ordnungswert_Nation",
            "Ordnungswert_Stufe",
            "Ordnungswert_Klasse",
            "Name",
        ],
        inplace=True,
    )


# Funktion zur Berechnung des Hashes der Datei
def calculate_file_hash(file):
    file_content = file.read()  # gesamten Inhalt lesen
    file.seek(
        0
    )  # zurück zum Anfang, damit Streamlit die Datei weiter verarbeiten kann
    return hashlib.md5(file_content).hexdigest()  # MD5-Hash berechnen


#
# ==================== Funktionen für die Anzeigen ====================
#


def update_schiffsregister():
    schiffsregister_aktuell_df = pd.DataFrame(
        st.session_state.schiffsregister_aktuell, columns=all_columns
    )

    if schiffsregister_aktuell_df.empty:
        placeholder_schiffsregister_aktuell.empty()
        placeholder_schiffsregister_aktuell.write("Noch keine Einträge")
    else:
        calculate_order_values(schiffsregister_aktuell_df)

        sort_dataframe(schiffsregister_aktuell_df)

        placeholder_schiffsregister_aktuell.empty()
        placeholder_schiffsregister_aktuell.dataframe(
            schiffsregister_aktuell_df
        )


def update_modification_displays():
    st.write("debugggg")
    original_df = pd.DataFrame(
        st.session_state.schiffsregister_original, columns=all_columns
    )
    st.dataframe(original_df)
    aktuell_df = pd.DataFrame(
        st.session_state.schiffsregister_aktuell, columns=all_columns
    )
    st.dataframe(aktuell_df)

    # Zugänge: Nicht in Original vorhandene Datensätze
    # zugaenge_df = pd.merge(
    #    original_df, aktuell_df, how="outer", indicator="Exist"
    # )
    # zugaenge_df = zugaenge_df.loc[zugaenge_df["Exist"] == "right_only"]

    # zugaenge_df = aktuell_df.merge(
    #    original_df, on=main_columns, how="left", indicator=True
    # )

    # Zugänge identifizieren: Alle Einträge, die ausschließlich im aktuellen Register vorkommen
    # Definieren Sie eine eindeutige Kombination für den Vergleich, hier z.B. alle Felder
    # zugaenge_df = aktuell_df[
    #    ~aktuell_df[main_columns]
    #    .apply(tuple, axis=1)
    #    .isin(original_df[main_columns].apply(tuple, axis=1))
    # ]
    zugaenge_df = aktuell_df[
        ~aktuell_df[main_columns].isin(original_df[main_columns]).all(axis=1)
    ]
    st.dataframe(zugaenge_df)
    print(zugaenge_df)
    # zugaenge_df = zugaenge_df[zugaenge_df["_merge"] == "left_only"].drop(
    #    columns=["_merge"]
    # )
    # st.write(zugaenge_df)

    if zugaenge_df.empty:
        placeholder_zugaenge.write("Keine Zugänge")
    else:
        calculate_order_values(zugaenge_df)
        sort_dataframe(zugaenge_df)
        placeholder_zugaenge.dataframe(zugaenge_df)

    # Veränderungen: Auf beiden Seiten einhaltene Datensätze, andere Werte
    common_entries = original_df[
        original_df[main_columns].isin(
            aktuell_df[main_columns].to_dict(orient="records")
        )
    ]
    veraenderungen_df = original_df.loc[common_entries.index].compare(
        aktuell_df.loc[common_entries.index],
        align_axis=0,
        keep_shape=False,
        keep_equal=True,
    )
    st.write(veraenderungen_df)


def update_veraenderungen():
    original_df = pd.DataFrame(
        st.session_state.schiffsregister_original, columns=all_columns
    )
    aktuell_df = pd.DataFrame(
        st.session_state.schiffsregister_aktuell, columns=all_columns
    )
    # Identifiziere nur Datensätze, die in beiden DataFrames vorhanden sind
    common_entries = original_df[
        original_df[main_columns].isin(
            aktuell_df[main_columns].to_dict(orient="records")
        )
    ]

    if common_entries.empty:
        placeholder_veraenderungen.empty()
        placeholder_veraenderungen.write("Keine Veränderungen")
    else:
        # Sicherstellen, dass beide DataFrames denselben Index haben
        veraenderungen_df = original_df.loc[common_entries.index].compare(
            aktuell_df.loc[common_entries.index],
            align_axis=0,
            keep_shape=False,
            keep_equal=True,
        )
        if veraenderungen_df.empty:
            placeholder_veraenderungen.empty()
            placeholder_veraenderungen.write("Keine Veränderungen")
        else:
            calculate_order_values(veraenderungen_df)

            # sort_dataframe(veraenderungen_df)

            # Anzeige aktualisieren
            placeholder_veraenderungen.empty()
            placeholder_veraenderungen.dataframe(veraenderungen_df)


def update_abgaenge():
    original_df = pd.DataFrame(
        st.session_state.schiffsregister_original, columns=all_columns
    )
    aktuell_df = pd.DataFrame(
        st.session_state.schiffsregister_aktuell, columns=all_columns
    )
    abgaenge_df = pd.merge(
        original_df, aktuell_df, how="outer", indicator="Exist"
    )
    abgaenge_df = abgaenge_df.loc[abgaenge_df["Exist"] == "left_only"]

    if abgaenge_df.empty:
        placeholder_abgaenge.empty()
        placeholder_abgaenge.write("Keine Abgänge")
    else:
        calculate_order_values(abgaenge_df)

        sort_dataframe(abgaenge_df)

        placeholder_abgaenge.empty()
        placeholder_abgaenge.dataframe(abgaenge_df)


#
# ========== Funktionen für die Bearbeitung von Einträgen ==========
#


def edit_entry(index):
    st.session_state.edit_index = index
    entry = st.session_state.schiffsregister_aktuell[index]
    st.session_state.edit_form_data = entry


def save_edited_entry():
    st.session_state.edit_form_result = False
    index = st.session_state.edit_index

    if not st.session_state.edit_form_data["Name"].strip():
        st.error("Der Name darf nicht leer sein.")
        return

    st.session_state.schiffsregister_aktuell[
        index
    ] = st.session_state.edit_form_data
    st.session_state.edit_form_result = True

    update_schiffsregister()
    # update_zugaenge()
    # update_veraenderungen()
    # update_abgaenge()

    st.session_state.pop("edit_index", None)
    st.session_state.pop("edit_form_data", None)


def update_edit_selectbox():
    selected_edit_index = placeholder_edit_selectbox.selectbox(
        "Wählen Sie einen Eintrag zum Bearbeiten aus",
        options=range(len(st.session_state.schiffsregister_aktuell)),
        format_func=lambda i: st.session_state.schiffsregister_aktuell[i][
            "Name"
        ],
    )
    return selected_edit_index


#
# ========== Funktionen für die Löschung von Einträgen ==========
#


def delete_entry(index):
    del st.session_state.schiffsregister_aktuell[index]


def update_delete_selectbox():
    selected_delete_index = placeholder_delete_selectbox.selectbox(
        "Wählen Sie einen Schiffseintrag zum Entfernen aus",
        options=range(len(st.session_state.schiffsregister_aktuell)),
        format_func=lambda i: st.session_state.schiffsregister_aktuell[i][
            "Name"
        ],
    )
    return selected_delete_index


#
# ========== Funktionen für die Download buttons ==========
#


def update_changes_download_button():
    zugaenge_text = ""
    veraenderungen_text = ""
    abgaenge_text = ""

    original_df = pd.DataFrame(
        st.session_state.schiffsregister_original, columns=all_columns
    )
    aktuell_df = pd.DataFrame(
        st.session_state.schiffsregister_aktuell, columns=all_columns
    )

    zugaenge_df = pd.merge(
        original_df, aktuell_df, how="outer", indicator="Exist"
    )
    zugaenge_df = zugaenge_df.loc[zugaenge_df["Exist"] == "right_only"]

    if zugaenge_df.empty:
        zugaenge_text = "Keine Zugänge\n"
    else:
        calculate_order_values(zugaenge_df)
        sort_dataframe(zugaenge_df)
        zugaenge_text = zugaenge_df.to_csv(
            sep=" ",
            columns=main_columns,
            index=False,
            header=False,
        )

    common_entries = original_df[
        original_df[main_columns].isin(
            aktuell_df[main_columns].to_dict(orient="records")
        )
    ]
    veraenderungen_df = original_df.loc[common_entries.index].compare(
        aktuell_df.loc[common_entries.index],
        align_axis=0,
        keep_shape=True,
        keep_equal=True,
    )

    if veraenderungen_df.empty:
        veraenderungen_text = "Keine Veränderungen\n"
    else:
        veraenderungen_text = veraenderungen_df.to_csv(
            sep=" ",
            columns=main_columns,
            index=False,
            header=False,
        )

    abgaenge_df = pd.merge(
        original_df, aktuell_df, how="outer", indicator="Exist"
    )
    abgaenge_df = abgaenge_df.loc[abgaenge_df["Exist"] == "left_only"]

    if abgaenge_df.empty:
        abgaenge_text = "Keine Abgänge\n"
    else:
        abgaenge_text = abgaenge_df.to_csv(
            sep=" ",
            columns=main_columns,
            index=False,
            header=False,
        )

    download_text = (
        f"Zugänge:"
        f"\n{zugaenge_text}"
        f"\nVeränderungen:"
        f"\n{veraenderungen_text}"
        f"\nAbgänge:"
        f"\n{abgaenge_text}"
    )

    placeholder_changes_text.empty()
    placeholder_changes_text.code(download_text)

    placeholder_changes_download_button.download_button(
        label=f"Bestandsänderungen herunterladen",
        data=download_text.encode("utf-8"),
        file_name=f'{time.strftime("%Y_%m_%d-%H_%M")}-Bestandsaenderungen.txt',
        mime="text/plain",
    )


# ==================== Skriptstart ====================

initialize_session_state()

placeholder_changes_text = None
placeholder_changes_download_button = None

with st.sidebar:
    st.header("Schiffsregister")
    st.html(
        f'<ul><li><a href="#aktueller-schiffsbestand">aktueller Schiffsbestand</a></li>'
        f'<li><a href="#zugaenge">Zugänge</a></li>'
        f'<li><a href="#veraenderungen">Veränderungen</a></li>'
        f'<li><a href="#abgaenge">Abgänge</a><br />&nbsp;</li>'
        f'<li><a href="#neues-schiff-eintragen">Neues Schiff eintragen</a></li>'
        f'<li><a href="#schiffseintrag-bearbeiten">Schiff bearbeiten</a></li>'
        f'<li><a href="#schiff-entfernen">Schiff entfernen</a></li>'
        f'<li><a href="#downloads">Downloadbereich</a></li>'
        f"</ul>"
    )

# Überschrift für die Anwendung
st.title("Schiffsregister")

if st.button("Neues Schiffsregister anlegen"):
    st.session_state.schiffsregister_original = []
    st.session_state.schiffsregister_aktuell = []
    st.success("Ein neues, leeres Schiffsregister wurde erstellt.")

uploaded_file = st.file_uploader(
    "Oder bestehendes Schiffsregister hochladen", type="csv"
)

if uploaded_file is not None:
    # Berechnung des Hashes der hochgeladenen Datei
    current_file_hash = calculate_file_hash(uploaded_file)

    # Prüfen, ob der Hash der Datei unterschiedlich ist
    if current_file_hash != st.session_state.last_uploaded_file_hash:
        # Es handelt sich um eine neue Datei:
        #     Flag zurücksetzen und Hash speichern
        st.session_state.file_processed = False
        st.session_state.last_uploaded_file_hash = current_file_hash

    # Datei nur einmalig verarbeiten, falls noch nicht geschehen
    if not st.session_state.file_processed:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            # Auf wichtige Spalten prüfen
            if all(column in uploaded_df.columns for column in main_columns):
                st.session_state.schiffsregister_original = []
                st.session_state[
                    "schiffsregister_original"
                ] = uploaded_df.to_dict("records")

                st.session_state.schiffsregister_aktuell = []
                st.session_state[
                    "schiffsregister_aktuell"
                ] = uploaded_df.to_dict("records")

                # Flag auf True setzen, um die Datei nicht erneut zu verarbeiten
                st.session_state.file_processed = True
            else:
                missing_columns = [
                    col
                    for col in main_columns
                    if col not in uploaded_df.columns
                ]
                st.error(
                    f"Die hochgeladene Datei enthält nicht die folgenden erforderlichen Spalten: {', '.join(missing_columns)}."
                )
        except Exception as e:
            st.error(f"Fehler beim Einlesen der Datei: {e}")


# Unterpunkt für den aktuellen Bestand
st.header("Aktueller Schiffsbestand")

schiffsregister_aktuell_df = pd.DataFrame(
    st.session_state.schiffsregister_aktuell, columns=all_columns
)

placeholder_schiffsregister_aktuell = st.empty()

update_schiffsregister()

st.subheader("Zugänge", "zugaenge")

zugaenge_df = pd.DataFrame(columns=all_columns)

placeholder_zugaenge = st.empty()

# update_zugaenge()

st.subheader("Veränderungen", "veraenderungen")

veraenderungen_df = pd.DataFrame(columns=all_columns)

placeholder_veraenderungen = st.empty()
# print(f'{time.strftime("%Y_%m_%d-%H_%M")}  vor update_veränderungen')
# update_veraenderungen()
# print(f'{time.strftime("%Y_%m_%d-%H_%M")}  nach update_veränderungen')

st.subheader("Abgänge", "abgaenge")

abgaenge_df = pd.DataFrame(columns=all_columns)

placeholder_abgaenge = st.empty()

# update_abgaenge()
update_modification_displays()
#
# ==================== Schiff hinzufügen ====================
#
st.subheader("Neues Schiff eintragen")

with st.form(key="new_ship_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        nation = st.selectbox("Nation", list(nations_order_dict.keys()))
        typ = st.selectbox("Typ", ship_type_options)
        klasse = st.selectbox("Klasse", list(ship_class_order_dict.keys()))
    with col2:
        stufe = st.selectbox("Stufe", list(ship_tier_order_dict.keys()))
        name = st.text_input("Name")

    submitted_form_new = st.form_submit_button("Schiff eintragen")

    if submitted_form_new:
        if not name.strip():
            st.error("Der Name darf nicht leer sein.")
        else:
            st.session_state.schiffsregister_aktuell.append(
                {
                    "Nation": nation,
                    "Typ": typ,
                    "Klasse": klasse,
                    "Stufe": stufe,
                    "Name": name,
                }
            )
            st.success(f"{name} erfolgreich eingetragen!")

            update_schiffsregister()
            # update_zugaenge()
            # update_veraenderungen()
            update_modification_displays()


#
# ==================== Schiff bearbeiten ====================
#
st.subheader("Schiffseintrag bearbeiten")

placeholder_edit_selectbox = st.empty()

selected_edit_index = update_edit_selectbox()

# Button zur Auswahl des Eintrags
if st.button("Eintrag laden"):
    edit_entry(selected_edit_index)

# Bearbeitungsformular, das sich nur zeigt, wenn ein Eintrag geladen wurde
if st.session_state.edit_index is not None:
    with st.form("edit_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.session_state.edit_form_data["Nation"] = st.selectbox(
                "Nation",
                list(nations_order_dict.keys()),
                index=list(nations_order_dict.keys()).index(
                    st.session_state.edit_form_data["Nation"]
                ),
            )
            st.session_state.edit_form_data["Typ"] = st.selectbox(
                "Typ",
                ship_type_options,
                index=ship_type_options.index(
                    st.session_state.edit_form_data["Typ"]
                ),
            )
            st.session_state.edit_form_data["Klasse"] = st.selectbox(
                "Klasse",
                list(ship_class_order_dict.keys()),
                index=list(ship_class_order_dict.keys()).index(
                    st.session_state.edit_form_data["Klasse"]
                ),
            )

        with col2:
            st.session_state.edit_form_data["Stufe"] = st.selectbox(
                "Stufe",
                list(ship_tier_order_dict.keys()),
                index=list(ship_tier_order_dict.keys()).index(
                    st.session_state.edit_form_data["Stufe"]
                ),
            )
            st.session_state.edit_form_data["Name"] = st.text_input(
                "Name", value=st.session_state.edit_form_data["Name"]
            )

        # Speichern-Button im Bearbeitungsformular
        submitted_edit = st.form_submit_button("Änderungen speichern")

        if submitted_edit:
            name_str = st.session_state.edit_form_data["Name"]
            save_edited_entry()
            if st.session_state.edit_form_result:
                st.success(f"Änderungen an '{name_str}' gespeichert.")

                update_schiffsregister()
                # update_zugaenge()
                # update_veraenderungen()
                # update_changes_download_button()
                update_modification_displays()


#
# ==================== Schiff entfernen ====================
#
st.subheader("Schiff entfernen")

placeholder_delete_selectbox = st.empty()

selected_delete_index = update_delete_selectbox()

# Prüfen, ob ein Eintrag ausgewählt wurde
if selected_delete_index is not None:
    # Bestätigungsabfrage für die Löschung wird nur angezeigt, wenn ein Eintrag ausgewählt wurde
    confirm_delete = st.radio(
        "Sind Sie sicher, dass Sie dieses Schiff entfernen möchten?",
        options=["Nein", "Ja"],
        index=0,
    )

    # Button zum Löschen des ausgewählten Eintrags, wenn bestätigt
    if confirm_delete == "Ja" and st.button("Schiff endgültig entfernen"):
        delete_entry(selected_delete_index)

        st.session_state.selected_delete_index = None
        st.session_state.selected_edit_index = None

        st.success("Schiff erfolgreich entfernt.")

        update_schiffsregister()
        update_zugaenge()
        update_veraenderungen()
        update_delete_selectbox()
        update_edit_selectbox()

    elif confirm_delete == "Nein":
        st.info("Schiff wird nicht entfernt.")
else:
    st.info("Bitte wählen Sie zuerst einen Eintrag aus, um ihn zu löschen.")

#
# ==================== Downloadbereich ====================
#
st.subheader("Downloads", "downloads")

placeholder_changes_text = st.empty()
placeholder_changes_download_button = st.empty()

update_changes_download_button()

csv = schiffsregister_aktuell_df.to_csv(
    columns=main_columns, index=False
).encode("utf-8")

st.download_button(
    label="Aktuelles Schiffsregister als CSV-Datei herunterladen",
    data=csv,
    file_name=f'{time.strftime("%Y_%m_%d-%H_%M")}-Schiffsregister.csv',
    mime="text/csv",
)

st.header("*** Debug Area ***")

st.write(st.session_state)
