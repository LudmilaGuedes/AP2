import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Diretórios base do projeto
BASE_DIR = Path(__file__).parent.parent.resolve()
BACK_DIR = str(BASE_DIR / "backend")
FRONT_DIR = str(BASE_DIR / "frontend")
LOG_DIR = str(BASE_DIR / "logs")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Token da API

# Configuração de logs
LOG_FILE = LOG_DIR + "/app.log"

# Garante que o diretório de logs existe
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,  # Nome do arquivo de log
    filemode="a",  # Modo de escrita no arquivo (append)
)

logger = logging.getLogger(__name__)

# Validações básicas
if not TOKEN:
    logger.error("Token de autenticação não encontrado no arquivo .env.")
    raise ValueError("Token de autenticação não encontrado no arquivo .env.")

logger.info("Configuração carregada com sucesso.")
