import math
import streamlit as st
import pandas as pd
import numpy as np

st.write("# 💵Simulador de Empréstimo")
col1, col2, col3 = st.columns(3)
valor_depositado = col1.number_input("Valor a Depositar (Em R$)", min_value=1.0)
prazo_emprestimo = col2.number_input("Prazo do Empréstimo (Em anos)", min_value=2)

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

for i in range(1, numero_de_pagamentos + 1):
    pagamento_juros = resto_balanca * juros_por_mes
    pagamento_principal = pagamento_mensal - pagamento_juros
    resto_balanca -= pagamento_principal
    ano = math.ceil(i / 12)  # Calculate the year into the loan
    agenda.append(
        [
            i,
            pagamento_mensal,
            pagamento_principal,
            pagamento_juros,
            resto_balanca,
            ano,
        ]
    )

df = pd.DataFrame(
    agenda,
    
    columns=["pagamento_mensal", "pagamento_principal", "pagamento_juros", "Interest", "resto_balanca", "ano"],
)

# Display the data-frame as a chart.
st.write("### Agenda de Pagamento")
pagamentos_df = df[["ano", "resto_balanca"]].groupby("ano").min()
st.line_chart(pagamentos_df)
col1, col2, col3 = st.columns(3)
col2.text("Prazo em Anos 🗓️")