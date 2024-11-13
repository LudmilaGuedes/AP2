import streamlit as st
from datetime import date
from backend.views import agrupar_dados, pegar_df_preco_corrigido
import pandas as pd
import matplotlib.pyplot as plt

def mostrar_pagina():
    st.header("Gráficos de Preço de Fechamento")
    st.write("Esta página exibirá gráficos baseados no preço de fechamento das ações da sua carteira e do Ibovespa.")

    # Verifica se a carteira está no session_state
    if 'carteira' not in st.session_state:
        st.error("Primeiro, gere a carteira na página de 'Estratégia'.")
        return

    # Recupera a carteira salva no session_state
    carteira = st.session_state['carteira']

    # Inputs para data de início e fim
    data_ini = st.date_input('Data Inicial', value=date(2023, 1, 1))
    data_fim = st.date_input('Data Final', value=date(2023, 12, 31))

    # Carrega o DataFrame de preços
    df_preco = pegar_df_preco_corrigido(data_ini, data_fim, carteira)
    df_grafico = agrupar_dados(data_ini, data_fim, carteira, df_preco)
    
    # Verifica se há dados no DataFrame
    if df_grafico.empty:
        st.error("Nenhum dado encontrado para o período selecionado.")
        return

    # Botão para gerar gráficos
    if st.button('Gerar Gráficos'):
        plt.figure(figsize=(10, 6))

        # Plota o preço de fechamento total da carteira
        plt.plot(df_grafico['data'], df_grafico['fechamento'], label='Carteira')

        # Adiciona o preço de fechamento do Ibovespa ao gráfico
        if 'fechamento_ibovespa' in df_grafico.columns:
            plt.plot(df_grafico['data'], df_grafico['fechamento_ibovespa'], label='Ibovespa', linestyle='--')

        # Adiciona título, rótulos e legenda
        plt.title("Preço de Fechamento da Carteira e do Ibovespa", fontsize=14)
        plt.xlabel("Data", fontsize=12)
        plt.ylabel("Preço de Fechamento", fontsize=12)
        plt.legend()

        # Exibe o gráfico no Streamlit
        st.pyplot(plt)

        # Limpa o gráfico após exibição
        plt.close()