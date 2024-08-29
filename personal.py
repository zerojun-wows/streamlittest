import streamlit as st
import pandas as pd

df_columns = [
    "Name",
    "Stufe(0-21)",
    "akt. Schiff",
    "Nation",
    "Nationenwert",
    "Gesamtwert",
]

Nations = {
    "JAPAN": 13,
    "USA": 12,
    "UDSSR": 11,
    "DEUTSCHLAND": 10,
    "GB": 9,
    "FRANKREICH": 8,
    "ITALIEN": 7,
    "PANASIEN": 6,
    "EUROPA": 5,
    "DIE NIEDERLANDE": 4,
    "COMMONWEALTH": 3,
    "PANAMERIKA": 2,
    "SPANIEN": 1,
}


def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def set_nationenwert(nation_name):
    return Nations[nation_name]


st.title("Personal Dashboard")

uploaded_file = st.file_uploader("Wähle eine Personal Datei", type="csv")

if uploaded_file is not None:
    st.write("Datei geladen.")
    df = pd.read_csv(uploaded_file)

    st.subheader("Dateneditor")
    config = {
        "Name": st.column_config.TextColumn("Name (benötigt)", required=True),
        "Stufe(0-21)": st.column_config.NumberColumn(
            "Stufe (0-21)", min_value=0, max_value=21, required=True
        ),
        "akt. Schiff": st.column_config.TextColumn("Akt. Schiff"),
        "Nation": st.column_config.SelectboxColumn("Nation", options=Nations),
        "Nationenwert": st.column_config.NumberColumn(
            "Nationenwert", min_value=1, max_value=13
        ),
        "Gesamtwert": st.column_config.NumberColumn(
            "Gesamtwert", min_value=1, max_value=34
        ),
    }

    result = st.data_editor(
        df, key="my_key", column_config=config, num_rows="dynamic"
    )

    #    st.write(st.session_state["my_key"])

    if st.button("Get results"):
        result["Nationenwert"] = result["Nation"].apply(set_nationenwert)
        result["Gesamtwert"] = result.apply(
            lambda x: x["Nationenwert"] + x["Stufe(0-21)"], axis=1
        )

        st.write(result)

        st.subheader("Daten Zusammenfassung")
        st.write(result.describe())

        st.subheader("Personal Datei")
        csv = convert_df(result)

        st.download_button(
            "Datei herunterladen",
            csv,
            "personal.csv",
            "text/csv",
            key="download-csv",
        )
else:
    st.write("Personal Datei muss hochgeladen werden")

    csv = convert_df(pd.DataFrame([], columns=df_columns))

    st.download_button(
        "Leere Personal Datei herunterladen",
        csv,
        "personal.csv",
        "text/csv",
        key="download-csv",
    )
