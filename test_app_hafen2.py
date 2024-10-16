import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Titel der Anwendung
st.title("Schiffe im Hafen")

# Wargaming API Informationen (ersetze diese durch deinen echten API_KEY und ACCOUNT_ID)
API_KEY = "db1926f579c2fb86bb8f2fad9b6f42e8"
ACCOUNT_ID = "572142053"


# Übersetzungen für Schiffstypen und Nationen
ship_type_translation = {
    "AirCarrier": "Flugzeugträger",
    "Battleship": "Schlachtschiff",
    "Cruiser": "Kreuzer",
    "Destroyer": "Zerstörer",
    "Submarine": "U-Boot",
}

nation_translation = {
    "usa": "USA",
    "ussr": "UDSSR",  # Schreibweise geändert
    "japan": "JAPAN",
    "germany": "DEUTSCHLAND",
    "uk": "GROßBRITANNIEN",
    "france": "FRANKREICH",
    "italy": "ITALIEN",
    "europe": "EUROPA",
    "pan_asia": "PAN-ASIEN",
    "pan_america": "PAN-AMERIKA",
    "commonwealth": "COMMONWEALTH",
    "netherlands": "NIEDERLANDE",  # Fehlende Nation ergänzt
    "spain": "SPANIEN",  # Fehlende Nation ergänzt
}


# Funktion, um die Schiffsstatistiken aus der API abzurufen
def get_ship_data():
    url = f"https://api.worldofwarships.eu/wows/ships/stats/?application_id={API_KEY}&account_id={ACCOUNT_ID}&language=de&r_realm=eu"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"Fehler beim Abrufen der Schiffsstatistiken: {response.status_code}"
        )
        return None


# Funktion, um die Schiffsdetails aus der API abzurufen
def get_ship_details(ship_id):
    url = f"https://api.worldofwarships.eu/wows/encyclopedia/ships/?application_id={API_KEY}&ship_id={ship_id}&language=de"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("data", {})
        if data:
            return data.get(str(ship_id), {})
        else:
            st.warning(f"Keine Details für Schiff {ship_id} gefunden.")
            return None
    else:
        st.error(
            f"Fehler beim Abrufen der Schiffsdetails für Schiff {ship_id}: {response.status_code}"
        )
        return None


# Funktion, um die Schiffsdaten in einem Pandas DataFrame zu speichern und anzuzeigen
def display_ships_in_dataframe(ships):
    if ships:
        # Erstelle eine Liste von Dictionaries, um sie in einen DataFrame zu konvertieren
        ship_list = []

        # Fortschrittsanzeige initialisieren
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_ships = len(ships)

        for idx, ship_info in enumerate(ships):
            ship_id = ship_info.get("ship_id", "Unbekannte ID")
            battles = ship_info.get("battles", 0)
            distance = ship_info.get("distance", 0)
            last_battle_time = ship_info.get("last_battle_time", None)
            updated_at = ship_info.get("updated_at", None)

            # Abrufen der Schiffsdetails (Name, Typ, Stufe, Nation, Preis)
            details = get_ship_details(ship_id)
            if details:  # Fehlerbehandlung falls 'details' None ist
                ship_name = details.get("name", "Unbekannter Name")
                ship_type = details.get("type", "Unbekannter Typ")
                tier = details.get("tier", "Unbekannte Stufe")
                nation = details.get("nation", "Unbekannte Nation")
                is_premium = details.get("is_premium", False)
                is_special = details.get("is_special", False)

                # Übersetze Schiffstyp und Nation
                ship_type = ship_type_translation.get(
                    ship_type, "Unbekannter Typ"
                )
                nation = nation_translation.get(
                    nation, "Unbekannte Nation"
                ).upper()  # Nation in Großbuchstaben

                # Preisinformationen (in Kredits oder Gold)
                price_credit = details.get("price_credit", "Nicht verfügbar")
                price_gold = details.get("price_gold", "Nicht verfügbar")

            else:
                ship_name = "Unbekannter Name"
                ship_type = "Unbekannter Typ"
                tier = "Unbekannte Stufe"
                nation = "Unbekannte Nation"
                is_premium = False
                is_special = False
                price_credit = "Nicht verfügbar"
                price_gold = "Nicht verfügbar"

            # Konvertiere die Zeitstempel in ein lesbares Datum
            if last_battle_time:
                last_battle_time = datetime.utcfromtimestamp(
                    last_battle_time
                ).strftime("%Y-%m-%d %H:%M:%S")
            if updated_at:
                updated_at = datetime.utcfromtimestamp(updated_at).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            # Füge die Schiffsdetails zur Liste hinzu
            ship_list.append(
                {
                    "Schiffs-ID": ship_id,
                    "Schiffsname": ship_name,
                    "Schiffstyp": ship_type,
                    "Schiffsstufe": tier,
                    "Schiffsnation": nation,
                    "Gefechte": battles,
                    "Zurückgelegte Meilen": distance,
                    "Letztes Gefecht": last_battle_time,
                    "Zuletzt aktualisiert": updated_at,
                    "Premiumschiff": "Ja" if is_premium else "Nein",
                    "Spezialschiff": "Ja" if is_special else "Nein",
                    "Kosten (Kredits)": price_credit,
                    "Kosten (Dublonen)": price_gold,
                }
            )

            # Fortschrittsbalken aktualisieren
            progress_bar.progress((idx + 1) / total_ships)
            status_text.text(f"Schiff {idx + 1} von {total_ships} verarbeitet")

        # Fortschrittsanzeige abschließen
        progress_bar.empty()
        status_text.text("Verarbeitung abgeschlossen, Daten werden geladen...")

        # Konvertiere die Liste in einen DataFrame
        df = pd.DataFrame(ship_list)

        # Datentypen der Schiffsstufe korrigieren (nicht-numerische Stufen zu NaN setzen)
        df["Schiffsstufe"] = pd.to_numeric(df["Schiffsstufe"], errors="coerce")

        # Filter hinzufügen
        st.sidebar.header("Filter")
        selected_type = st.sidebar.selectbox(
            "Schiffstyp", ["Alle"] + list(ship_type_translation.values())
        )
        selected_nation = st.sidebar.selectbox(
            "Schiffsnation", ["Alle"] + list(nation_translation.values())
        )
        selected_tier = st.sidebar.selectbox(
            "Schiffsstufe",
            ["Alle"] + sorted(df["Schiffsstufe"].dropna().astype(int).unique()),
        )
        selected_premium = st.sidebar.selectbox(
            "Premiumschiff", ["Alle", "Ja", "Nein"]
        )
        selected_special = st.sidebar.selectbox(
            "Spezialschiff", ["Alle", "Ja", "Nein"]
        )

        # Filter anwenden
        if selected_type != "Alle":
            df = df[df["Schiffstyp"] == selected_type]
        if selected_nation != "Alle":
            df = df[df["Schiffsnation"] == selected_nation]
        if selected_tier != "Alle":
            df = df[df["Schiffsstufe"] == int(selected_tier)]
        if selected_premium != "Alle":
            df = df[df["Premiumschiff"] == selected_premium]
        if selected_special != "Alle":
            df = df[df["Spezialschiff"] == selected_special]

        # DataFrame in Streamlit anzeigen
        st.subheader("Schiffsübersicht:")
        st.dataframe(df)  # DataFrame mit Streamlit anzeigen

    else:
        st.write("Keine Schiffe im Hafen gefunden.")


# Daten abrufen
ship_data = get_ship_data()

if ship_data and "data" in ship_data:
    # Zugriff auf die Schiffe des Spielers - 'data' enthält eine Liste von Schiffen
    ships = ship_data["data"].get(str(ACCOUNT_ID), [])
    display_ships_in_dataframe(ships)
else:
    st.error(
        "Die API-Antwort enthält keine Schiffdaten oder es ist ein Fehler aufgetreten."
    )
