# config.py

import json
import logging

logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logger.error("Arquivo de configuração 'config.json' não encontrado.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar o arquivo de configuração: {e}")
        return None
