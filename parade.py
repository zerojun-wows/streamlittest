import streamlit as st
import pandas as pd
import time

df_columns = [
    "Name",
    "Bindestrich",
    "Typ",
    "Artikel",
    "Bezeichnung",
    "Stufe",
    "Typwert",
    "Stufewert",
]

editor_column_order = ["Name", "Typ", "Stufe"]

ship_type_order_values = {
    "U-Boot": 1,
    "Zerstörer": 2,
    "Kreuzer": 3,
    "Schlachtschiff": 4,
    "Flugzeugträger": 5,
}

tier_order_values = {
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


def get_ship_type_value(ship_type):
    return ship_type_order_values[ship_type]


def get_tier_value(tier):
    return tier_order_values[tier]


df = pd.DataFrame([], columns=df_columns)

st.title("zerojuns parade test")

st.subheader("Dateneditor")
config = {
    "Name": st.column_config.TextColumn("Name (benötigt)", required=True),
    "Typ": st.column_config.SelectboxColumn(
        "Typ", options=ship_type_order_values, required=True
    ),
    "Stufe": st.column_config.SelectboxColumn(
        "Stufe", options=tier_order_values, required=True
    ),
}

result = st.data_editor(
    df,
    key="my_key",
    column_order=editor_column_order,
    column_config=config,
    num_rows="dynamic",
)

if st.button("Erstellen"):
    result["Bindestrich"] = "-"
    result["Artikel"] = "der"
    result["Bezeichnung"] = "Stufe"
    result["Typwert"] = result["Typ"].apply(get_ship_type_value)
    result["Stufewert"] = result["Stufe"].apply(get_tier_value)

    sorted_df = result.sort_values(by=["Stufewert", "Typwert", "Name"])
    cleaned_df = sorted_df.drop(["Stufewert", "Typwert"], axis=1)

    st.subheader("Erfasste sortierte Daten")
    st.write(cleaned_df)

    csv = cleaned_df.to_csv(sep=" ", index=False, header=False).encode("utf-8")

    st.download_button(
        "Datei herunterladen",
        csv,
        f"parade{time.time()}.csv",
        "text/csv",
        key="download-csv",
    )
