import streamlit as st
import pandas as pd
from sr_data_config import all_columns


def find_new_entries():
    """
    Funktion zur Ermittlung der neuen Datensätze in schiffsregister_aktuell,
    die nicht in schiffsregister_original enthalten sind.
    """
    if (
        "schiffsregister_original" in st.session_state
        and "schiffsregister_aktuell" in st.session_state
    ):
        original_df = pd.DataFrame(
            st.session_state.schiffsregister_original, columns=all_columns
        )
        aktuell_df = pd.DataFrame(
            st.session_state.schiffsregister_aktuell, columns=all_columns
        )

        # Indizes der neuen Datensätze ermitteln
        neue_indizes = aktuell_df.index.difference(original_df.index)

        # Zugänge speichern
        added_df = aktuell_df.loc[neue_indizes]

        # Speichern der Zugänge im Session State
        st.session_state["added_df"] = added_df


def find_modified_entries():
    """
    Findet geänderte Datensätze im Schiffsregister.
    """
    if (
        "schiffsregister_original" in st.session_state
        and "schiffsregister_aktuell" in st.session_state
    ):
        original_df = pd.DataFrame(
            st.session_state.schiffsregister_original, columns=all_columns
        )
        aktuell_df = pd.DataFrame(
            st.session_state.schiffsregister_aktuell, columns=all_columns
        )

        # Gemeinsame Indizes finden
        gemeinsame_indizes = original_df.index.intersection(aktuell_df.index)

        # Unterschiede identifizieren
        changes_df = original_df.loc[gemeinsame_indizes].compare(
            aktuell_df.loc[gemeinsame_indizes]
        )
        st.session_state["changes_df"] = changes_df


def find_deleted_entries():
    """
    Findet gelöschte Datensätze im Schiffsregister.
    """
    if (
        "schiffsregister_original" in st.session_state
        and "schiffsregister_aktuell" in st.session_state
    ):
        original_df = pd.DataFrame(
            st.session_state.schiffsregister_original, columns=all_columns
        )
        aktuell_df = pd.DataFrame(
            st.session_state.schiffsregister_aktuell, columns=all_columns
        )

        # Indizes der gelöschten Datensätze
        deleted_indices = original_df.index.difference(aktuell_df.index)
        deleted_df = original_df.loc[deleted_indices]

        st.session_state["deleted_df"] = deleted_df
