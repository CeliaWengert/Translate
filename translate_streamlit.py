import streamlit as st
import pandas as pd

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    df = pd.read_excel(uploaded_file)

    st.dataframe(df)
