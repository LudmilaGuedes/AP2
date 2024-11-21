import streamlit as st
from backend.views import gerar_carteira
from backend.utils import validar_dia_util
from datetime import datetime,date

def mostrar_estrategia():
    """
    Exibe a página de estratégia para criação de carteiras de investimentos.
    """
    st.title("💼 Estratégia de Investimento")
    st.write("""
        Nesta página, você pode criar uma carteira de investimentos baseada na estratégia da Magic Formula.
        Escolha os indicadores desejados e a quantidade de ações na carteira.
    """)

    # Lista de feriados estáticos (exemplo para 2024 no Brasil)
    feriados = [
        "2024-01-01", "2024-02-13", "2024-03-29", "2024-04-21", "2024-05-01",
        "2024-09-07", "2024-10-12", "2024-11-02", "2024-11-15", "2024-12-25"
    ]
    feriados = [datetime.strptime(data, "%Y-%m-%d").date() for data in feriados]

    # Inputs do usuário
    st.header("📌 Parâmetros da Estratégia")

    # Selectbox para o indicador de rentabilidade
    indicador_rentabilidade = st.selectbox(
        "Escolha o Indicador de Rentabilidade:",
        options=["roe", "roc", "roic"],
        index=0
    )

    # Selectbox para o indicador de desconto
    indicador_desconto = st.selectbox(
        "Escolha o Indicador de Desconto:",
        options=["earning_yield", "dividend_yield", "p_vp"],
        index=0
    )

    # Input para quantidade de ações na carteira
    quantidade_acoes = st.number_input(
        "Quantidade de Ações na Carteira:",
        min_value=1,
        max_value=20,
        value=10,
        step=1
    )

    # Data base para os dados do planilhão
    data_base = st.date_input("Selecione a Data Base:",value = date(2024,1,2))

    # Validação da Data Base (feriados e finais de semana)
    if not validar_dia_util(data_base, feriados):
        st.error("A data selecionada é inválida (feriado ou final de semana). Por favor, escolha outra data.")
        return

    st.header("📊 Carteira Gerada")
    st.markdown("""
        Após configurar os parâmetros acima, clique no botão para gerar a carteira.
        Os resultados serão exibidos abaixo em formato de tabela interativa.
    """)

    # Botão para gerar a carteira
    if st.button("Gerar Carteira"):
        with st.spinner("Gerando a carteira..."):
            try:
                # Gera a carteira
                df_carteira = gerar_carteira(
                    data_base.strftime('%Y-%m-%d'),
                    indicador_rentabilidade,
                    indicador_desconto,
                    quantidade_acoes
                )

                if df_carteira.empty:
                    st.warning("Nenhuma carteira gerada.")
                else:
                    # Armazena a Carteira no session_state
                    st.session_state["carteira"] = df_carteira

                    # Exibe a Carteira
                    st.write("### Carteira de Investimentos:")
                    st.dataframe(df_carteira)
            except Exception as e:
                st.error(f"Erro ao gerar a carteira: {e}")


    st.header("📘 O Que é a Magic Formula?")
    st.write("""
        A Magic Formula é uma estratégia de investimento desenvolvida por Joel Greenblatt e apresentada em seu livro 
        *"The Little Book That Beats the Market"*. Ela combina dois fatores principais para identificar ações 
        subvalorizadas e com alto potencial de retorno:
    """)

    st.subheader("🔍 Fatores Principais:")
    st.markdown("""
    1. **Rentabilidade (Indicadores de Qualidade):** A capacidade de uma empresa gerar lucros em relação ao capital investido.
       Exemplos: *ROE*, *ROC*, *ROIC*.
    2. **Desconto (Indicadores de Valuation):** Mede o quão barata uma ação está em relação ao seu valor intrínseco.
       Exemplos: *Earning Yield*, *Dividend Yield*, *P/VP*.
    """)

    st.subheader("💡 Vantagens da Magic Formula:")
    st.markdown("""
    - **Simples e Objetiva:** Utiliza apenas dois fatores para selecionar ações.
    - **Baseada em Dados:** Fundamentada em princípios sólidos de finanças.
    - **Resultados Consistentes:** Estudos mostram que a estratégia supera muitos benchmarks de mercado.
    - **Adaptável:** Pode ser ajustada para diferentes mercados e preferências pessoais.
    """)

    st.header("📂 Informações Adicionais")
    st.markdown("""
    - A carteira gerada neste sistema segue os princípios da Magic Formula.
    - Personalize os parâmetros para adaptar a estratégia às suas preferências.
    - Para mais informações, entre em contato com o suporte.
    """)
