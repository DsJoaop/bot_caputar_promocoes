import json
import logging
import os

logger = logging.getLogger(__name__)


def load_config():
    try:
        script_dir = os.path.dirname(__file__)  # Obtém o diretório do script atual
        file_path = os.path.join(script_dir, 'settings.json')  # Caminho absoluto para o settings.json

        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logger.error("Arquivo de configuração 'settings.json' não encontrado.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar o arquivo de configuração: {e}")
        return None