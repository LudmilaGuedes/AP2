# setup_paths.py
import sys
from pathlib import Path

# Define o diretório base e o diretório backend
BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / 'frontend'
BACK_DIR = BASE_DIR / 'backend'

# Adiciona os diretórios ao sys.path
sys.path.extend([str(BASE_DIR), str(FRONT_DIR), str(BACK_DIR)])
