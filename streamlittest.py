#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: 
Author: zerojun
Date Created: 
Date Modified: 
Version: 0.0.0
Python Version: 
Dependencies: 
License: 
"""

# import standard library modules
# import 3rd party modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# import local modules


st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.write("File uploaded...")
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("Generate Chart"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])

else:
    st.write("Waiting on file upload")


csv = convert_df(df)

st.download_button(
   "Datei herunterladen",
   csv,
   "personal.csv",
   "text/csv",
   key='download-csv'
)
