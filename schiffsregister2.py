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


# Funktion zur Aktualisierung des DataFrames im Session State
def update_dataframe():
    df = pd.DataFrame(st.session_state.schiffsregister, columns=all_columns)
    st.rerun()


def get_new_entries_string() -> str:
    try:
        if new_entries_df.empty:
            pass
    except NameError:
        return "keine Zugänge\n"
    else:
        if new_entries_df.empty:
            return "keine Zugänge\n"
        else:
            return new_entries_df.to_csv(sep=" ", header=False, index=False)


def get_modified_entries_string() -> str:
    try:
        if modified_entries_df.empty:
            pass
    except NameError:
        return "keine Veränderungen\n"
    else:
        return modified_entries_df.to_csv(sep=" ", header=False, index=False)


def get_deleted_entries_string() -> str:
    try:
        if deleted_entries_df.empty:
            pass
    except NameError:
        return "keine Abgänge\n"
    else:
        return deleted_entries_df.to_csv(sep=" ", header=False, index=False)


# Beispielhafte leere Datenliste für den Schiffsbestand
if "schiffsregister" not in st.session_state:
    st.session_state.schiffsregister = []


# Überschrift für die Anwendung
st.title("Schiffsregister")


# Unterpunkt für den aktuellen Bestand
st.subheader("Aktueller Bestand")

if "success" in st.session_state:
    st.success(st.session_state.success)
    del st.session_state["success"]

# Erstelle den DataFrame mit den allen Spalten
df = pd.DataFrame(st.session_state.schiffsregister, columns=all_columns)

# Berechne die Ordnungswerte
df["Ordnungswert_Nation"] = df["Nation"].map(nations_order_dict)
df["Ordnungswert_Klasse"] = df["Klasse"].map(ship_class_order_dict)
df["Ordnungswert_Stufe"] = df["Stufe"].map(ship_tier_order_dict)

# Sortiere das DataFrame nach den Ordnungswerten und Namen
df.sort_values(
    by=[
        "Ordnungswert_Nation",
        "Ordnungswert_Stufe",
        "Ordnungswert_Klasse",
        "Name",
    ],
    inplace=True,
)

# entferne Ordnungsspalten
df.drop(
    columns=hidden_columns,
    inplace=True,
)


# Konfiguriere die Eingabemöglichkeiten des Dataeditors
config_columns = {
    "Nation": st.column_config.SelectboxColumn(
        "Nation", options=nations_order_dict, required=True
    ),
    "Typ": st.column_config.SelectboxColumn(
        "Typ", options=ship_type_options, required=True
    ),
    "Klasse": st.column_config.SelectboxColumn(
        "Klasse", options=ship_class_order_dict, required=True
    ),
    "Stufe": st.column_config.SelectboxColumn(
        "Stufe", options=ship_tier_order_dict, required=True
    ),
    "Name": st.column_config.TextColumn("Name", required=True),
}

# Zeige den DataFrame mit der st.data_editor Komponente an
edited_df = st.data_editor(
    df,
    key="editor",
    num_rows="dynamic",
    use_container_width=True,
    column_config=config_columns,
    hide_index=False,
)


st.subheader("Zugänge")

new_entries_df = pd.DataFrame(st.session_state.editor["added_rows"])

if new_entries_df.empty:
    st.write("keine Zugänge")
else:
    st.dataframe(new_entries_df)


st.subheader("Veränderungen")

if not st.session_state.editor["edited_rows"]:
    st.write("keine Veränderungen")
else:
    index_list = list(st.session_state.editor["edited_rows"].keys())

    # edited_df filtern nach 'edited_rows'
    edited_new_df = edited_df.filter(items=index_list, axis=0)
    # df filtern nach 'edited_rows'
    edited_old_df = df.filter(items=index_list, axis=0)

    modified_entries_df = edited_new_df.compare(
        edited_old_df,
        align_axis=0,
        keep_shape=True,
        keep_equal=True,
        result_names=("aktueller Eintrag", "vorheriger Eintrag"),
    )

    st.dataframe(modified_entries_df)


st.subheader("Abgänge")

if not st.session_state.editor["deleted_rows"]:
    st.write("keine Abgänge")
else:
    index_list = list(st.session_state.editor["deleted_rows"])

    # df filtern nach 'deleted_rows'
    deleted_entries_df = df.filter(items=index_list, axis=0)

    st.dataframe(deleted_entries_df)


st.subheader("Datenübernahme & -export")

changes_text_export_values = (
    f"Zugänge\n"
    + get_new_entries_string()
    + f"\nVeränderungen\n"
    + get_modified_entries_string()
    + f"\nAbgänge\n"
    + get_deleted_entries_string()
)

st.text_area(
    "Zugänge, Veränderungen und Abgänge textexport",
    changes_text_export_values,
)

# Button zur Übernahme der Änderungen
if st.button("Alle Veränderungen übernehmen"):
    st.session_state.schiffsregister = edited_df.to_dict("records")
    st.session_state.success = "Änderungen erfolgreich übernommen!"
    st.rerun()

if st.button("Nur Änderungen verwerfen"):
    if st.session_state.editor["edited_rows"]:
        st.session_state.editor["edited_rows"] = {}
        st.session_state.success = "Nur Veränderungen zurückgesetzt!"
        # st.rerun()

if st.button("Nur Abgänge verwerfen"):
    if st.session_state.editor["deleted_rows"]:
        del st.session_state.editor["deleted_rows"]
        st.session_state.editor["deleted_rows"] = []
        # edited_df = pd.concat([edited_df, deleted_entries_df])
        st.session_state.success = "Nur Abgänge zurückgesetzt!"
        # st.rerun()
        update_dataframe()


# remove when ready
st.subheader("Debug")


# st.write(df)

st.write(st.session_state)
