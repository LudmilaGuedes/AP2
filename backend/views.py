import pandas as pd
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)
from apis import (obter_dados_planilhao,obter_preco_corrigido,obter_preco_ibovespa)


def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (defau

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = obter_dados_planilhao(data_base)
    if dados:
        dados = dados['dados']
        planilhao = pd.DataFrame(dados)
        planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
        df = filtrar_duplicado(planilhao)
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return df
    else:
        logger.info(f"Sem Dados no Planilhão: {data_base}")
        print(f"Sem Dados no Planilhão: {data_base}")
    

def pegar_df_preco_corrigido(data_ini:date, data_fim:date, carteira:list):
    """
    Consulta os preços Corrigidos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    print(f"Consultando as seguintes ações: {carteira}")
    for ticker in carteira:
        print(f"Consultando dados para a ação: {ticker}")

        dados = obter_preco_corrigido(ticker, data_ini, data_fim)
        if dados:
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco


def pegar_df_preco_diversos(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos

    params:

    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = obter_preco_ibovespa(data_ini, data_fim, ticker)
        if dados:
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco
 

def gerar_carteira(indicador_rentabilidade, indicador_desconto, data_inicio, quantidade_acoes):
    """
    Gera uma carteira com as melhores ações com base na Magic Formula:
    usa o indicador de rentabilidade e o indicador de desconto.

    Params:
    - indicador_rentabilidade (str): Indicador de rentabilidade escolhido (ex: 'roe', 'roc', 'roic').
    - indicador_desconto (str): Indicador de desconto escolhido (ex: 'earning_yield', 'dividend_yield', 'p_vp').
    - data_inicio (str): Data de início da análise no formato 'YYYY-MM-DD' (para consulta na API, não utilizado no DataFrame).
    - quantidade_acoes (int): Quantidade de ações a serem selecionadas para a carteira.

    Returns:
    - pd.DataFrame: DataFrame contendo as ações selecionadas para a carteira.
    """
    
    # Obter os dados do planilhão
    df = pegar_df_planilhao(data_inicio)

    # Verificando se os indicadores escolhidos estão na lista de colunas do DataFrame
    if indicador_rentabilidade not in df.columns or indicador_desconto not in df.columns:
        raise ValueError(f"Um ou ambos os indicadores não estão disponíveis no DataFrame: '{indicador_rentabilidade}', '{indicador_desconto}'.")

    # Calculando o ranking para cada indicador
    df['ranking_rentabilidade'] = df[indicador_rentabilidade].rank()
    df['ranking_desconto'] = df[indicador_desconto].rank()  # Menor valor é melhor para desconto

    # Calculando a soma dos rankings
    df['ranking'] = df['ranking_rentabilidade'] + df['ranking_desconto']
    
    # Ordenando as ações com base no ranking total
    df_ordenado = df.sort_values(by='ranking',ascending=False)
    df_final = df_ordenado[['ticker','setor','roc','roe','roic','earning_yield','dividend_yield','p_vp','ranking']]
    # Selecionar as melhores ações com base na quantidade especificada
    df_final = df_final.head(quantidade_acoes).reset_index(drop=True)  # Resetando índice
    df_final.index = df_final.index + 1
    carteira = df_final

    return carteira


logger = logging.getLogger(__name__)

def agrupar_dados(data_ini, data_fim, carteira, df_preco):
    """
    Agrupa dados de preço de fechamento das ações e do Ibovespa durante o período especificado.
    """
    try:
        # Verificação de DataFrame vazio
        if df_preco.empty:
            raise ValueError("O DataFrame de preços está vazio. Verifique os dados fornecidos.")
        
        # Converte datas para o tipo datetime
        df_preco['data'] = pd.to_datetime(df_preco['data'], errors='coerce')
        data_ini = pd.to_datetime(data_ini)
        data_fim = pd.to_datetime(data_fim)
        
        # Filtro para o intervalo de datas
        df_preco_filtrado = df_preco[(df_preco['data'] >= data_ini) & (df_preco['data'] <= data_fim)]
        
        if df_preco_filtrado.empty:
            logger.warning("Nenhum dado encontrado para o intervalo de datas selecionado.")
            return pd.DataFrame()
        
        # Agrupando os dados de fechamento da carteira por data
        df_grafico = df_preco_filtrado.groupby("data")['fechamento'].sum().reset_index()
        
        # Obter os dados do Ibovespa e adicionar ao gráfico
        dados_ibovespa = obter_preco_ibovespa(data_ini, data_fim)
        if dados_ibovespa:
            df_ibovespa = pd.DataFrame(dados_ibovespa)
            df_ibovespa['data'] = pd.to_datetime(df_ibovespa['data'], errors='coerce')
            df_ibovespa = df_ibovespa[['data', 'fechamento']].rename(columns={'fechamento': 'fechamento_ibovespa'})

            # Mescla os dados de ações e do Ibovespa com base na data, usando outer join para incluir todas as datas
            df_grafico = pd.merge(df_grafico, df_ibovespa, on='data', how='outer').sort_values(by='data')
            df_grafico.fillna(method='ffill', inplace=True)  # Preenche valores ausentes no Ibovespa e na carteira
        else:
            logger.warning("Dados do Ibovespa não encontrados para o período selecionado.")
        
    except Exception as e:
        logger.error(f"Erro ao agrupar dados: {e}")
        raise
    
    return df_grafico







# carteira = gerar_carteira('roc','earning_yield','2024-09-09',30)
# carteira_pc =[]
# for ticker in carteira['ticker']:
#     carteira_pc.append(ticker)

# print(carteira_pc)
# pegar_df_preco_corrigido('2024-11-04','2024-11-06',carteira['ticker'])

# df = pegar_df_planilhao('2024-09-09')

# # Verificando se os indicadores escolhidos estão na lista de colunas do DataFrame

# # Calculando o ranking para cada indicador
# df['ranking_rentabilidade'] = df['roc'].rank()
# df['ranking_desconto'] = df['earning_yield'].rank()  

# # Calculando a soma dos rankings
# df['ranking'] = df['ranking_rentabilidade'] + df['ranking_desconto']

# # Ordenando as ações com base no ranking total
# df = df.sort_values(['ranking'],ascending=False).reset_index(drop=True)[:30]
# df_final = df[['ticker','setor','roc','roe','roic','earning_yield','dividend_yield','p_vp','ranking_rentabilidade','ranking_desconto','ranking']]
# # Selecionar as melhores ações com base na quantidade especificada
# carteira = df_final






