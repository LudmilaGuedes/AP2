import requests
from backend.config import TOKEN, logger  # Importa o token e o logger do config.py
import pandas as pd

def obter_dados_planilhao(data_base):
    """
    Consulta o planilhão com base na data fornecida.

    Args:
        data_base (str): Data base para consulta no formato 'YYYY-MM-DD'.

    Returns:
        response (requests.Response): Resposta da API contendo os dados do planilhão.
    """
    url = "https://laboratoriodefinancas.com/api/v1/planilhao"
    headers = {'Authorization': f'JWT {TOKEN}'}
    params = {'data_base': data_base}
    
    try:
        logger.info(f"Consultando o planilhão para a data base: {data_base}")
        response = requests.get(url, params=params, headers=headers)
        
        # Validação básica da resposta
        if response.status_code != 200:
            logger.error(f"Erro ao consultar o planilhão: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        logger.info("Consulta ao planilhão realizada com sucesso.")
        return pd.DataFrame(response.json()['dados'])
    except Exception as e:
        logger.error(f"Erro ao obter dados do planilhão: {e}")
        raise


def obter_preco_corrigido(ticker, data_ini, data_fim):
    """
    Consulta o preço corrigido de um ticker no período fornecido.

    Args:
        ticker (str): Código do ativo (ex.: PETR4).
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        response.json()['dados']: Resposta da API contendo os dados dos preços corrigidos.
    """
    url = "https://laboratoriodefinancas.com/api/v1/preco-corrigido"
    headers = {'Authorization': f'JWT {TOKEN}'}
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    
    try:
        logger.info(f"Consultando preços corrigidos para {ticker} de {data_ini} a {data_fim}")
        response = requests.get(url, params=params, headers=headers)
        
        # Validação básica da resposta
        if response.status_code != 200:
            logger.error(f"Erro ao consultar preços corrigidos: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        logger.info("Consulta de preços corrigidos realizada com sucesso.")
        return pd.DataFrame(response.json()['dados'])
    except Exception as e:
        logger.error(f"Erro ao obter preços corrigidos: {e}")
        raise


def obter_preco_ibovespa(data_ini, data_fim):
    """
    Consulta os preços históricos do Ibovespa no período fornecido.

    Args:
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        response.json()['dados']: Resposta da API contendo os preços do Ibovespa.
    """
    url = "https://laboratoriodefinancas.com/api/v1/preco-diversos"
    headers = {'Authorization': f'JWT {TOKEN}'}
    params = {'ticker': 'ibov', 'data_ini': data_ini, 'data_fim': data_fim}
    
    try:
        logger.info(f"Consultando preços do Ibovespa de {data_ini} a {data_fim}")
        response = requests.get(url, params=params, headers=headers)
        
        # Validação básica da resposta
        if response.status_code != 200:
            logger.error(f"Erro ao consultar preços do Ibovespa: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        logger.info("Consulta de preços do Ibovespa realizada com sucesso.")
        return pd.DataFrame(response.json()['dados'])
    except Exception as e:
        logger.error(f"Erro ao obter preços do Ibovespa: {e}")
        raise


