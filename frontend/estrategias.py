# frontend/estrategia_page.py
import streamlit as st
from backend.views import gerar_carteira
import pandas as pd

def mostrar_pagina():
    st.title("Estratégia de Investimento")

    # Campos de entrada
    indicador_rentabilidade = st.selectbox("Selecione o Indicador de Rentabilidade:", ['roe', 'roc', 'roic'])
    indicador_desconto = st.selectbox("Selecione o Indicador de Desconto:", ['earning_yield', 'dividend_yield', 'p_vp'])
    
    data_inicio = st.date_input("Data de Início:")
    quantidade_acoes = st.number_input("Quantidade de Ações na Carteira:", min_value=1, value=10)

    if st.button("Gerar Carteira"):
        try:
            # Chamar a função para gerar a carteira com a data de início
            carteira = gerar_carteira(indicador_rentabilidade, indicador_desconto, data_inicio.strftime('%Y-%m-%d'), quantidade_acoes)

            # Armazenar a carteira no session_state
            carteira_lista = carteira['ticker'].tolist()
            st.session_state['carteira'] = carteira_lista  # Salva a carteira para uso em outra página

            # Exibir a carteira gerada
            st.subheader("Carteira Gerada:")
            st.write(carteira)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
