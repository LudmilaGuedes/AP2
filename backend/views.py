import pandas as pd
from backend.apis import obter_dados_planilhao, obter_preco_corrigido, obter_preco_ibovespa
from backend.config import logger


def filtrar_duplicadas(df):
    """
    Filtra as ações duplicadas no DataFrame, selecionando a de maior volume.

    Args:
        df (pd.DataFrame): DataFrame com as ações brutas.

    Returns:
        pd.DataFrame: DataFrame sem duplicatas, mantendo apenas as ações com maior volume.
    """
    logger.info("Iniciando filtragem de ações duplicadas com base no volume.")
    try:
        # Adiciona uma coluna base para identificar duplicatas (ignora o número final no ticker)
        df['base_ticker'] = df['ticker'].str.extract(r'([A-Z]+)')
        
        # Seleciona a ação com o maior volume dentro dos duplicados
        df_filtrado = (
            df.sort_values(by='volume', ascending=False)  # Ordena por volume decrescente
            .drop_duplicates(subset='base_ticker', keep='first')  # Mantém o maior volume por base_ticker
        )
        
        # Remove a coluna auxiliar e reinicia os indices começando em 1
        df_filtrado.drop(columns=['base_ticker'], inplace=True)
        df_filtrado.reset_index(drop=True, inplace=True)  # Reinicia os índices
        df_filtrado.index = df_filtrado.index + 1  # Ajusta para começar em 1
        
        logger.info(f"Filtragem de duplicatas concluída. Total de ações restantes: {len(df_filtrado)}")
        return df_filtrado
    except Exception as e:
        logger.error(f"Erro ao filtrar ações duplicadas: {e}")
        raise


def pegar_planilhao_filtrado(data_base, setores=None):
    """
    Obtém o DataFrame do planilhão filtrado, com duplicatas removidas e setores opcionais.

    Args:
        data_base (str): Data base para consulta no formato 'YYYY-MM-DD'.
        setores (list): Lista de setores para filtrar (opcional).

    Returns:
        pd.DataFrame: DataFrame do planilhão filtrado e limpo.
    """
    logger.info(f"Obtendo planilhão filtrado para a data base: {data_base}")
    try:
        # Obtém o DataFrame bruto do planilhão
        df_planilhao = obter_dados_planilhao(data_base)

        # Verifica se o DataFrame retornou vazio
        if df_planilhao.empty:
            logger.warning(f"Planilhão vazio para a data base: {data_base}")
            return pd.DataFrame()

        # Filtra duplicatas
        df_filtrado = filtrar_duplicadas(df_planilhao)

        # Filtra por setores, se fornecido
        if setores:
            logger.info(f"Filtrando setores: {setores}")
            df_filtrado = df_filtrado[df_filtrado['setor'].isin(setores)]

        logger.info(f"Planilhão filtrado com sucesso. Total de ações: {len(df_filtrado)}")
        return df_filtrado
    except Exception as e:
        logger.error(f"Erro ao obter e filtrar o planilhão: {e}")
        raise


def pegar_preco_corrigido(lista_tickers, data_ini, data_fim):
    """
    Obtém os dados de preço corrigido para uma lista de tickers no período fornecido.

    Args:
        lista_tickers (list): Lista de códigos dos ativos (ex.: ['PETR4', 'VALE3']).
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame contendo os preços corrigidos de todos os tickers, com índices reiniciados.
    """
    logger.info(f"Obtendo preços corrigidos para {len(lista_tickers)} tickers de {data_ini} a {data_fim}")
    try:
        # Lista para armazenar os DataFrames individuais
        lista_dfs = []

        for ticker in lista_tickers:
            logger.info(f"Consultando preços corrigidos para {ticker}")
            try:
                # Obter preços corrigidos para o ticker atual
                df_precos = obter_preco_corrigido(ticker, data_ini, data_fim)
                df_precos['ticker'] = ticker  # Adiciona o ticker ao DataFrame
                lista_dfs.append(df_precos)
            except Exception as e:
                logger.warning(f"Erro ao consultar preços corrigidos para {ticker}: {e}")
                continue

        # Combina todos os DataFrames em um único DataFrame
        if lista_dfs:
            df_final = pd.concat(lista_dfs, ignore_index=True)
            df_final.reset_index(drop=True, inplace=True)  # Reinicia os índices
            logger.info(f"Preços corrigidos obtidos com sucesso para todos os tickers. Total de registros: {len(df_final)}")
            return df_final
        else:
            logger.warning("Nenhum dado de preço corrigido foi obtido para os tickers fornecidos.")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erro ao obter preços corrigidos para a lista de tickers: {e}")
        raise

def pegar_dados_ibovespa(data_ini, data_fim):
    """
    Obtém os dados de preço histórico do Ibovespa no período fornecido.

    Args:
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame contendo os preços históricos do Ibovespa, com índices reiniciados.
    """
    logger.info(f"Obtendo dados do Ibovespa de {data_ini} a {data_fim}")
    try:
        # Chama a API para obter os preços do Ibovespa
        df_ibovespa = obter_preco_ibovespa(data_ini, data_fim)
        
        # Verifica se o DataFrame está vazio
        if df_ibovespa.empty:
            logger.warning(f"Nenhum dado do Ibovespa encontrado para o período de {data_ini} a {data_fim}.")
            return pd.DataFrame()
        
        # Reinicia os índices
        df_ibovespa.reset_index(drop=True, inplace=True)
        logger.info(f"Dados do Ibovespa obtidos com sucesso. Total de registros: {len(df_ibovespa)}")
        return df_ibovespa
    except Exception as e:
        logger.error(f"Erro ao obter dados do Ibovespa: {e}")
        raise

def gerar_carteira(data_base, indicador_rentabilidade, indicador_desconto, quantidade_acoes):
    """
    Gera uma carteira de investimentos utilizando a Magic Formula.

    Args:
        data_base (str): Data base para consulta no formato 'YYYY-MM-DD'.
        indicador_rentabilidade (str): Indicador de rentabilidade (ex.: 'roe' ou 'roic').
        indicador_desconto (str): Indicador de desconto (ex.: 'earning_yield' ou 'dividend_yield').
        quantidade_acoes (int): Número de ações na carteira.

    Returns:
        pd.DataFrame: DataFrame contendo as ações selecionadas para a carteira, com rankings.
    """
    logger.info(f"Gerando carteira para a data base: {data_base}, "
                f"com indicadores {indicador_rentabilidade} e {indicador_desconto}, "
                f"selecionando {quantidade_acoes} ações.")
    try:
        # Obtém o DataFrame filtrado do planilhão
        df_planilhao = pegar_planilhao_filtrado(data_base)

        # Verifica se o DataFrame está vazio
        if df_planilhao.empty:
            logger.warning(f"Planilhão retornou vazio para a data base: {data_base}")
            return pd.DataFrame()

        # Gera rankings individuais para os indicadores
        logger.info("Calculando rankings para os indicadores.")
        df_planilhao['ranking_rentabilidade'] = df_planilhao[indicador_rentabilidade].rank()
        df_planilhao['ranking_desconto'] = df_planilhao[indicador_desconto].rank()

        # Soma os rankings para obter o ranking final
        df_planilhao['ranking'] = df_planilhao['ranking_rentabilidade'] + df_planilhao['ranking_desconto']

        # Ordena pelo ranking final
        df_planilhao = df_planilhao.sort_values(by='ranking',ascending=False).reset_index(drop=True)
        df_planilhao = df_planilhao[['ticker','setor','roc','roe','roic','earning_yield','dividend_yield','p_vp','ranking']]
        # Seleciona as melhores ações para a carteira
        df_carteira = df_planilhao.head(quantidade_acoes)
        df_carteira.index = df_carteira.index + 1
        logger.info(f"Carteira gerada com sucesso. Total de ações selecionadas: {len(df_carteira)}")
        return df_carteira
    except Exception as e:
        logger.error(f"Erro ao gerar carteira: {e}")
        raise


def agrupar_dados(carteira, data_ini, data_fim):
    """
    Organiza os dados para o gráfico comparativo entre a carteira e o Ibovespa.

    Args:
        carteira (pd.DataFrame): DataFrame contendo os dados da carteira.
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame contendo as informações necessárias para o gráfico.
    """
    logger.info(f"Organizando dados para gráfico de {data_ini} a {data_fim}.")
    try:
        # Obter preços corrigidos para os tickers da carteira
        lista_tickers = carteira['ticker'].tolist()
        df_precos_carteira = pegar_preco_corrigido(lista_tickers, data_ini, data_fim)

        # Obter preços do Ibovespa
        df_ibovespa = pegar_dados_ibovespa(data_ini, data_fim)

        # Calcula o retorno acumulado para cada ticker na carteira
        logger.info("Calculando retorno acumulado para a carteira.")
        df_precos_carteira['retorno_acumulado'] = (
            df_precos_carteira.groupby('ticker')['fechamento']
            .transform(lambda x: x / x.iloc[0] - 1)
        )

        # Calcula o retorno acumulado médio da carteira
        df_carteira_agrupado = (
            df_precos_carteira.groupby('data')['retorno_acumulado']
            .mean()
            .reset_index()
            .rename(columns={'retorno_acumulado': 'retorno_acumulado_carteira'})
        )

        # Calcula o retorno acumulado para o Ibovespa usando a coluna 'fechamento'
        logger.info("Calculando retorno acumulado para o Ibovespa.")
        df_ibovespa['retorno_acumulado_ibovespa'] = (
            df_ibovespa['fechamento'] / df_ibovespa['fechamento'].iloc[0] - 1
        )

        # Junta os dados da carteira e do Ibovespa
        df_final = df_carteira_agrupado.merge(
            df_ibovespa[['data', 'retorno_acumulado_ibovespa']],
            on='data',
            how='inner'
        )

        logger.info("Dados organizados com sucesso para o gráfico.")
        return df_final  # Certifica-se de retornar apenas o DataFrame final
    except Exception as e:
        logger.error(f"Erro ao organizar dados para o gráfico: {e}")
        raise

import matplotlib.pyplot as plt

def gerar_grafico(df):
    """
    Gera um gráfico comparativo entre a Carteira e o Ibovespa.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'data', 
                           'retorno_acumulado_carteira', e 'retorno_acumulado_ibovespa'.

    Returns:
        None
    """
    try:
        # Converte a coluna 'data' para o formato datetime para plotagem
        df['data'] = pd.to_datetime(df['data'])

        # Configura o gráfico
        plt.figure(figsize=(12, 6))
        
        # Plota o retorno acumulado da carteira
        plt.plot(
            df['data'], df['retorno_acumulado_carteira'] * 100, label="Carteira", linewidth=2
        )

        # Plota o retorno acumulado do Ibovespa
        plt.plot(
            df['data'], df['retorno_acumulado_ibovespa'] * 100, label="Ibovespa", linestyle="--", linewidth=2
        )

        # Configurações adicionais do gráfico
        plt.title("Retorno Acumulado: Carteira vs. Ibovespa", fontsize=16)
        plt.xlabel("Data", fontsize=12)
        plt.ylabel("Retorno Acumulado (%)", fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)

        # Exibe o gráfico
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")



data_base = '2024-11-13'
carteira_lista = ['VALE3','ITUB4','B3SA3']
data_ini = '2024-01-02'
data_fim = '2024-10-30'

df_planilhao = pegar_planilhao_filtrado(data_base)
setores_unicos = df_planilhao['setor'].unique().tolist()
df_preco_corrigido = pegar_preco_corrigido(carteira_lista,data_ini, data_fim)
df_preco_ibovespa = pegar_dados_ibovespa(data_ini,data_fim)
carteira = gerar_carteira(data_base, 'roc','earning_yield',10)
informacao_grafico = agrupar_dados(carteira, data_ini, data_fim)
gerar_grafico(informacao_grafico)


carteira.columns
df_preco_corrigido.columns
df_preco_ibovespa.columns