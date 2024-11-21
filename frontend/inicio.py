import streamlit as st

def mostrar_pagina_inicial():
    """
    Exibe o conteúdo da página inicial, com informações detalhadas e organizadas.
    """
    st.header("Projeto Final AP2 - Lucas Rodor, Bruno Ambrósio, Ludmila Guedes, Anna Clara Thimoteo")
    st.title("Bem-vindo ao Sistema de Análise Financeira 📊")
    st.write("""
        Este sistema foi desenvolvido para auxiliar investidores e analistas na tomada de decisões financeiras
        utilizando dados reais e estratégias comprovadas.
    """)

    st.header("📌 Funcionalidades Principais")
    st.markdown("""
    - **Planilhão**: Acesse dados financeiros detalhados de diversas ações.
    - **Estratégia**: Gere carteiras de investimento com base na Magic Formula.
    - **Gráficos**: Compare o desempenho da sua carteira com o Ibovespa.
    """)

    st.header("💡 Objetivos do Sistema")
    st.markdown("""
    1. Oferecer uma plataforma intuitiva e poderosa para análise de dados financeiros.
    2. Permitir a criação de carteiras otimizadas para maximizar retorno.
    3. Acompanhar o desempenho das carteiras em tempo real, com comparações claras e visuais.
    """)

    st.header("🚀 Como Utilizar")
    st.markdown("""
    1. Use o menu no topo para navegar entre as páginas:
        - **Planilhão**: Explore os dados detalhados das ações.
        - **Estratégia**: Crie sua carteira personalizada.
        - **Gráficos**: Visualize os resultados das suas análises.
    2. Insira os parâmetros necessários em cada página e obtenha os resultados de forma rápida e visual.
    3. Use os gráficos para interpretar o desempenho e tomar decisões informadas.
    """)

    st.header("📂 Organização do Sistema")
    st.markdown("""
    O sistema é dividido em módulos:
    - **Backend**: Processa os dados e integra com as APIs externas.
    - **Frontend**: Apresenta os dados de forma amigável e interativa.
    """)

    # Botão para explorar diretamente
    if st.button("Explorar Planilhão 🚀"):
        st.session_state["menu"] = "Planilhão"
