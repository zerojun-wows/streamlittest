import streamlit as st
import pandas as pd

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

ship_type_order_dict = {
    "standard": 1,
    "elite": 2,
    "premium": 3,
    "spezial": 4,
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

ship_register_columns = ["Nation", "Typ", "Klasse", "Stufe", "Name"]


def get_empty_ship_register():
    return (
        pd.DataFrame([], columns=ship_register_columns)
        .to_csv(index=False)
        .encode("utf-8")
    )


def check_columns_exist(base_df: pd.DataFrame, check_df: pd.DataFrame) -> bool:
    """
    Prüft, ob alle Spalten in check_df in base_df vorhanden sind.

    :param base_df: Das Basis-DataFrame, das die Spalten enthält.
    :param check_df: Das DataFrame, dessen Spalten überprüft werden.
    :return: True, wenn alle Spalten in check_df in base_df vorhanden sind, sonst False.
    """
    return check_df.columns.isin(base_df.columns).all()


#
# Streamlit script
#
st.title("Schiffsregisterverwaltung")
st.subheader("Schiffsregisteröffnung")

ship_register_file = st.file_uploader(
    "Wähle eine Schiffsregister Datei", type="csv"
)

if ship_register_file is None:
    st.write("Es muss eine Schiffsregister Datei eingereicht werden.")

    empty_ship_register_file = get_empty_ship_register()

    st.download_button(
        "Leere Schiffsregister Datei herunterladen",
        empty_ship_register_file,
        "shipregister.csv",
        "text/csv",
        key="download-csv",
    )
else:
    source_ship_register_dataframe = pd.read_csv(ship_register_file)

    st.subheader("Gültikeitsprüfung des Schiffsregisters")
    if not check_columns_exist(
        source_ship_register_dataframe,
        pd.DataFrame([], columns=ship_register_columns),
    ):
        st.write("Ungültiges Schiffsregister.")
    else:
        st.write("Gültiges Schiffsregister.")

        st.subheader("Erfassung von Änderungen im Schiffsregister")
        working_ship_register_dataframe = source_ship_register_dataframe.copy()

        editor_config = {
            "Nation": st.column_config.SelectboxColumn(
                "Nation", options=nations_order_dict, required=True
            ),
            "Typ": st.column_config.SelectboxColumn(
                "Typ", options=ship_type_order_dict, required=True
            ),
            "Klasse": st.column_config.SelectboxColumn(
                "Klasse", options=ship_class_order_dict, required=True
            ),
            "Stufe": st.column_config.SelectboxColumn(
                "Stufe", options=ship_tier_order_dict, required=True
            ),
            "Name": st.column_config.TextColumn(
                "Name (erforderlich)", required=True
            ),
        }

        result = st.data_editor(
            working_ship_register_dataframe,
            key="my_key",
            column_order=ship_register_columns,
            column_config=editor_config,
            num_rows="dynamic",
        )

        st.write(working_ship_register_dataframe.describe())
