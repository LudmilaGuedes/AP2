import streamlit as st
from streamlit_option_menu import option_menu
from frontend.inicio import mostrar_pagina_inicial
from frontend.planilhao import mostrar_planilhao
from frontend.estrategia import mostrar_estrategia
from frontend.graficos import mostrar_graficos

# Configuração inicial do app
st.set_page_config(page_title="Análise Financeira", layout="wide")

# Inicializa o estado no session_state
if "planilhao" not in st.session_state:
    st.session_state["planilhao"] = None

if "carteira" not in st.session_state:
    st.session_state["carteira"] = None

if "grafico" not in st.session_state:
    st.session_state["grafico"] = None

if "menu" not in st.session_state:
    st.session_state["menu"] = "Página Inicial"

# Menu principal na lateral (sidebar)
with st.sidebar:
    menu = option_menu(
        menu_title="Menu Principal",  # Título no menu
        options=["Página Inicial", "Planilhão", "Estratégia", "Gráficos"],
        icons=["house", "table", "briefcase", "bar-chart"],
        menu_icon="cast",
        default_index=["Página Inicial", "Planilhão", "Estratégia", "Gráficos"].index(st.session_state["menu"]),
        orientation="vertical",  # Menu vertical
    )

# Atualiza o estado do menu no session_state
st.session_state["menu"] = menu

# Navegação para as páginas
if menu == "Página Inicial":
    mostrar_pagina_inicial()
elif menu == "Planilhão":
    mostrar_planilhao()
elif menu == "Estratégia":
    mostrar_estrategia()
elif menu == "Gráficos":
    mostrar_graficos()
