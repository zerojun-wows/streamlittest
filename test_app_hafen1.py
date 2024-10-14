import streamlit as st
import requests

# Titel der Anwendung
st.title("World of Warships Schiffsübersicht")

# Wargaming API Informationen
API_KEY = "dein_api_key"
ACCOUNT_ID = "deine_account_id"


# Funktion, um die Schiffsstatistiken aus der API abzurufen
def get_ship_data():
    url = f"https://api.worldofwarships.eu/wows/ships/stats/?application_id={API_KEY}&account_id={ACCOUNT_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Daten abrufen
data = get_ship_data()

# Überprüfen, ob Daten erfolgreich geladen wurden
if data:
    ships = data["data"][str(ACCOUNT_ID)]
    # Liste aller Schiffe anzeigen
    st.write(f"Du hast {len(ships)} Schiffe.")

    # Details jedes Schiffs auflisten
    for ship in ships:
        st.subheader(ship["name"])
        st.write(f"Gefechte: {ship['battles']}")
        st.write(f"Siegquote: {ship['wins'] / ship['battles'] * 100:.2f}%")
else:
    st.error("Fehler beim Abrufen der Daten.")
