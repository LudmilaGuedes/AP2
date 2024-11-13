# frontend/planilhao_page.py
import streamlit as st
from backend.routers import menu_planilhao  # Função que consulta dados no Planilhão
import time

def mostrar_pagina():
    st.header("Consulta ao Planilhão")

    # Input de data
    data_base = st.date_input("Escolha a data: ")

    # Efeito de carregamento ao consultar o planilhão
    with st.spinner('Consultando os dados...'):
        try:
            df = menu_planilhao(data_base)
            if df.empty:
                st.warning("Nenhum dado encontrado para a data selecionada.")
            else:
                st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao consultar o planilhão: {e}")
