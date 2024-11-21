import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from datetime import date, timedelta, datetime
import pandas as pd
from backend.views import agrupar_dados
from backend.utils import validar_dia_util

def mostrar_graficos():
    """
    Exibe a página de gráficos para comparação do desempenho da carteira e do Ibovespa.
    """
    st.title("📈 Visualização de Gráficos")
    st.write("""
        Nesta página, você pode visualizar o desempenho acumulado da sua carteira de investimentos
        comparado ao Ibovespa em um período definido.
    """)

    # Lista de feriados estáticos (exemplo para 2024 no Brasil)
    feriados = [
        "2024-01-01", "2024-02-13", "2024-03-29", "2024-04-21", "2024-05-01",
        "2024-09-07", "2024-10-12", "2024-11-02", "2024-11-15", "2024-12-25"
    ]
    feriados = [datetime.strptime(data, "%Y-%m-%d").date() for data in feriados]

    # Inputs do usuário
    st.header("📌 Parâmetros para o Gráfico")

    # Data de início e fim com valores padrão
    data_ini = st.date_input("Selecione a Data Inicial:", value=date(2024, 1, 2))
    data_fim = st.date_input("Selecione a Data Final:", value=date.today() - timedelta(days=1))

    # Validação das datas
    if not validar_dia_util(data_ini, feriados):
        st.error("A Data Inicial selecionada é inválida (feriado ou final de semana). Por favor, escolha outra data.")
        return

    if not validar_dia_util(data_fim, feriados):
        st.error("A Data Final selecionada é inválida (feriado ou final de semana). Por favor, escolha outra data.")
        return

    if data_ini >= data_fim:
        st.warning("A data inicial deve ser anterior à data final.")
        return

    # Verifica se a carteira está no session_state
    if "carteira" not in st.session_state or st.session_state["carteira"] is None:
        st.error("Por favor, gere a carteira na página de Estratégia antes de visualizar os gráficos.")
        return

    # Botão para gerar o gráfico
    st.header("📊 Gráfico Comparativo")
    st.markdown("""
        Após configurar os parâmetros acima, clique no botão para visualizar o gráfico.
    """)

    if st.button("Gerar Gráfico"):
        with st.spinner("Gerando o gráfico...Isso pode levar alguns segundos"):
            try:
                # Gera os dados para o gráfico
                df_grafico = agrupar_dados(
                    st.session_state["carteira"], 
                    data_ini.strftime('%Y-%m-%d'), 
                    data_fim.strftime('%Y-%m-%d')
                )

                if df_grafico.empty:
                    st.warning("Nenhum dado encontrado.")
                else:
                    # Converte a coluna 'data' para datetime.date
                    df_grafico['data'] = pd.to_datetime(df_grafico['data']).dt.date

                    # Cria o layout para restringir o tamanho do gráfico na tela
                    col1, col2, col3 = st.columns([1, 2, 1])  # Espaçamento ao redor do gráfico

                    with col2:
                        st.markdown("#### Visualização do Gráfico")

                        # Gera o gráfico usando matplotlib
                        fig, ax = plt.subplots(figsize=(6, 3))  # Ajuste do tamanho do gráfico

                        # Linha da carteira
                        ax.plot(
                            df_grafico['data'], 
                            df_grafico['retorno_acumulado_carteira'] * 100, 
                            label="Carteira", 
                            linewidth=2
                        )

                        # Linha do Ibovespa
                        ax.plot(
                            df_grafico['data'], 
                            df_grafico['retorno_acumulado_ibovespa'] * 100, 
                            label="Ibovespa", 
                            linestyle="--", 
                            linewidth=2
                        )

                        # Configurações do gráfico
                        ax.set_title("Retorno Acumulado: Carteira vs. Ibovespa", fontsize=12)
                        ax.set_xlabel("Data", fontsize=10)
                        ax.set_ylabel("Retorno Acumulado (%)", fontsize=10)
                        ax.legend(fontsize=10)
                        ax.grid(True)

                        # Ajuste do eixo X
                        ax.set_xlim([data_ini, data_fim])  # Limita o eixo X às datas inputadas
                        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # Limita o número de rótulos no eixo X
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Formato das datas
                        plt.xticks(rotation=45)  # Rotaciona os rótulos para evitar sobreposição

                        # Exibe o gráfico no Streamlit
                        st.pyplot(fig)

            except Exception as e:
                st.error(f"Erro ao gerar o gráfico: {e}")

    # # Verifica se o gráfico já está armazenado
    # if "grafico" in st.session_state:
    #     st.write("### Dados do Gráfico Anterior:")
    #     st.dataframe(st.session_state["grafico"])

    st.header("📂 Informações Adicionais")
    st.markdown("""
    - O gráfico mostra o desempenho acumulado da carteira comparado ao Ibovespa no período selecionado.
    - Certifique-se de que a carteira foi gerada na página de Estratégia antes de criar o gráfico.
    - Para dúvidas ou problemas, entre em contato com o suporte.
    """)