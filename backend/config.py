import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent.resolve()
BACK_DIR = str(BASE_DIR)+ "/backend"
FRONT_DIR = str(BASE_DIR)+ "/frontend"
LOG_DIR= str(BASE_DIR)+ "/logs"
import logging #Configuração básica do logging
logging.basicConfig(level=logging.INFO,
                    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename = '(LOG_DIR)/app.log', #Nome do arquivo de LOG
                    filemode = 'a') 