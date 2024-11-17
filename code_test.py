import pandas as pd

# Beispielhafte Original- und Aktuell-DataFrames
original_df = pd.DataFrame(
    {
        "Nation": ["JAPAN", "JAPAN"],
        "Typ": ["elite", "standard"],
        "Klasse": ["Kreuzer", "Kreuzer"],
        "Stufe": ["I", "II"],
        "Name": ["Hashidate", "Chikuma"],
    }
)

aktuell_df = pd.DataFrame(
    {
        "Nation": ["JAPAN", "JAPAN", "JAPAN"],
        "Typ": ["elite", "elite", "standard"],
        "Klasse": ["Kreuzer", "Kreuzer", "U-Boot"],
        "Stufe": ["I", "II", "I"],
        "Name": ["Hashidate", "Chikuma", "ggg"],
    }
)

# Schritt 1: Finde die Zugänge
# Einträge im aktuell_df, die nicht im original_df existieren
zugaenge_df = aktuell_df[
    ~aktuell_df.apply(tuple, 1).isin(original_df.apply(tuple, 1))
]

# Schritt 2: Finde die geänderten Datensätze
# Vergleiche Werte aus dem original_df mit denen im aktuell_df
geandert_df = pd.merge(
    aktuell_df,
    original_df,
    on=["Nation", "Typ", "Klasse", "Stufe", "Name"],
    how="inner",
    indicator=True,
)
geandert_df = geandert_df[geandert_df["_merge"] == "both"]

# Die Zugänge und geänderten Datensätze ausgeben
print("Zugänge:")
print(zugaenge_df)
print("\nGeänderte Datensätze:")
print(geandert_df)
