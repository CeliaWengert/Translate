import streamlit as st
import pandas as pd

df = pd.read_excel(r'./NLDone.xlsx')

st.dataframe(df)