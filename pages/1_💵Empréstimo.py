import math
import streamlit as st
import pandas as pd
from vega_datasets import data


st.write("# 💵Simulador de Empréstimo")
col1, col2, col3 = st.columns(3)
valor_depositado = col1.number_input("Valor a Depositar (Em R$)", min_value=100, value=1000)
prazo_emprestimo = col2.number_input("Prazo do Empréstimo (Em anos)", min_value=2, value=6)

juros = col3.number_input("Juros (Em % por ano)", min_value=0.1, value=5.5)

juros_por_mes = (juros / 100) / 12
numero_de_pagamentos = prazo_emprestimo * 12
pagamento_mensal = (
    valor_depositado
    * (juros_por_mes * (1 + juros_por_mes) ** numero_de_pagamentos)
    / ((1 + juros_por_mes) ** numero_de_pagamentos - 1)
)

pagamento_total = pagamento_mensal * numero_de_pagamentos
juros_total = pagamento_total - valor_depositado

st.write("### Pagamentos")
col1, col2, col3 = st.columns(3)
col1.metric(label="Pagamento Mensal", value=f"R${pagamento_mensal:,.2f}")
col2.metric(label="Pagamento Total", value=f"R${pagamento_total:,.2f}")
col3.metric(label="Total de Juros", value=f"R${juros_total:,.2f}")

agenda = []
resto_balanca = valor_depositado

@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

for i in range(1, numero_de_pagamentos + 1):
    pagamento_juros = resto_balanca * juros_por_mes
    pagamento_principal = pagamento_mensal - pagamento_juros
    resto_balanca -= pagamento_principal
    ano = math.ceil(i / 12)  # Calculate the year into the loan
    date = get_data()
    agenda.append(
        [
            i,
            pagamento_mensal,
            pagamento_principal,
            pagamento_juros,
            resto_balanca,
            ano,
            date
        ]
    )

df = pd.DataFrame(
    agenda,
    
    columns=["i", "Pagamento Anual", "Dinheiro Investido", "Juros Cobrado", "A Pagar", "Anos", "date"],
    dtype=object
)


chart_data = df

st.bar_chart(
   chart_data, x="Anos", y=["Pagamento Anual", "Juros Cobrado"], color=["#FF5252", "#3976C8"])
