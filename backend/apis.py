import os
import requests
from dotenv import load_dotenv
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename = 'FILE')

logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('TOKEN')
if not token:
    logger.error("Token não encontrado. Verifique se o arquivo .env contém o TOKEN.")
    raise ValueError("Token não encontrado. Verifique se o arquivo .env contém o TOKEN.")

headers = {"Authorization": "JWT {}".format(token)}

def obter_dados_planilhao(data_base):
    """Consulta todas as ações com os principais indicadores fundamentalistas.
    Params: 
    data_base (date): data inputada pelo usuário para consultar os dados
    
    return:
    dados (list): lista com o dicionário de todas as ações ou uma lista vazia em caso de erro."""
    
    params = {'data_base': data_base}
    
    try:
        response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
        
        if response.status_code == 200:
            dados = response.json()
            logger.info(f"Dados do planilhão consultados com sucesso: {data_base}")
            print(f"Dados do planilhão consultados com sucesso: {data_base}")
            return dados if dados else []  # Retorna uma lista vazia se dados estiver vazio
        else:
            logger.error(f"Erro na consulta do planilhão: {data_base}. Status code: {response.status_code}")
            print(f"Erro na consulta do planilhão: {data_base}. Status code: {response.status_code}")
            return []  # Retorna uma lista vazia em caso de erro
    except Exception as e:
        logger.error(f"Erro na função obter_dados_planilhao: {e}")
        print(f"Erro na função obter_dados_planilhao: {e}")
        return []  # Retorna uma lista vazia em caso de exceção


def obter_preco_corrigido(ticker, data_ini, data_fim):
    """Função para obter os dados de preço de ações."""
    try:
        params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
        response = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
        

    except Exception:
        logger.error(f"Erro na função obter_preco_acoes: {Exception}")
        print(f"Erro na função obter_preco_acoes: {Exception}")

    return response.json()["dados"] if response.status_code == 200 else None

def obter_preco_ibovespa(data_ini, data_fim):
    """Função para obter os dados do IBOVESPA."""
    try: 
        params = {'ticker': 'ibov', 'data_ini': data_ini, 'data_fim': data_fim}
        response = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
        logger.info(f"Dados do planilhao consultados com sucesso: {data_ini} - {data_fim}")
        print ((f"Dados do planilhao consultados com sucesso: {data_ini} - {data_fim}"))
    except Exception:
        logger.error(f"Erro na função obter_preco_ibovespa: {Exception}")
        print(f"Erro na função obter_preco_ibovespa: {Exception}")
    return response.json()['dados'] if response.status_code == 200 else None


