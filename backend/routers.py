# routers.py
import streamlit as st
from backend.views import pegar_df_planilhao, gerar_carteira  # Importar a função gerar_carteira

def menu_planilhao(data_base):
    df = pegar_df_planilhao(data_base)
    return df 

def menu_gerar_carteira(indicador_rentabilidade, indicador_desconto, data_base, data_fim, quantidade_acoes):
    # Chama a função para gerar a carteira com os parâmetros recebidos
    carteira = gerar_carteira(indicador_rentabilidade, indicador_desconto, data_base, data_fim, quantidade_acoes)
    return carteira
