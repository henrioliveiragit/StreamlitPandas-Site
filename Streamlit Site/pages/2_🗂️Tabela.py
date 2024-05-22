import streamlit as st
import pandas as pd

st.write("# 🗂️Tabela Importada do Excel")
st.text("🐼 Usando Pandas 2.2.2")
df = pd.read_csv("Contoso - Lojas.csv", sep=';', encoding='utf-8-sig')

st.table(data=df)