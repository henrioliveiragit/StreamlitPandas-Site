import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')
from st_aggrid import AgGrid

st.write("# 💼Administração")

df_vendas = pd.read_csv("Contoso - Vendas - 2017.csv", sep=';', encoding='cp1252')
df_lojas = pd.read_csv("Contoso - Lojas.csv", sep=';', encoding='cp1252')
df_clientes = pd.read_csv("Contoso - Clientes.csv", sep=';', encoding='cp1252')
df_produtos = pd.read_csv("Contoso - Cadastro Produtos.csv", sep=";", encoding='cp1252')

df_lojas = df_lojas.rename(columns={'ÿID Loja' : 'ID Loja'})
df_clientes = df_clientes.rename(columns={'ÿID Cliente' : 'ID Cliente'})
df_clientes = df_clientes.drop(['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10'], axis=1)
df_produtos = df_produtos.rename(columns={'ÿNome do Produto' : 'Nome do Produto'})

df_resumo_total = df_vendas.merge(df_produtos, on="ID Produto")
df_resumo_total = df_resumo_total.merge(df_lojas, on="ID Loja")
df_resumo_total = df_resumo_total.merge(df_clientes, on="ID Cliente")

df_resumo_total = df_resumo_total.drop(columns=['ID Canal', "ID Loja", "ID Produto", "ID Promocao", "ID Cliente", "ID Subcategoria", "Quantidade Colaboradores", "Numero de Filhos", "Data de Nascimento"], axis=1)
df_resumo_total = df_resumo_total.rename(columns={'Numero da Venda' : 'ID Venda'})
df_resumo_total = df_resumo_total.rename(columns={'País' : 'Localização da Loja'})
df_resumo_total = df_resumo_total.rename(columns={'E-mail' : 'E-mail do Cliente'})


cols = st.columns([1])

height = 650

with cols[0]:
    tab = st.tabs(["Vendas", "Lojas", "Clientes", "Produtos", "Resumo Total das Transações"])
    
with tab[0]: tabela_vendas = AgGrid(df_vendas[:1000], height=height,
pagination=True,suppressMovableColumns=True)
with tab[1]: tabela_lojas = AgGrid(df_lojas[:1000], height=height,
pagination=True, fit_columns_on_grid_load=True,suppressMovableColumns=True)
with tab[2]: tabela_clientes = AgGrid(df_clientes[:1000], height=height,
pagination=True, fit_columns_on_grid_load=True,suppressMovableColumns=True)
with tab[3]: tabela_produtos = AgGrid(df_produtos[:1000], height=height,
pagination=True, fit_columns_on_grid_load=True,suppressMovableColumns=True)
with tab[4]: tabela_resumo = AgGrid(df_resumo_total[:1000], height=height,
pagination=True, fit_columns_on_grid_load=True,suppressMovableColumns=True)