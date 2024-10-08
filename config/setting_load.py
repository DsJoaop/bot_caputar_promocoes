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


def add_produto_desejo(product_link, max_price):
    config = load_config()
    if config is not None:
        if "desejos" not in config:
            config["desejos"] = []

        novo_produto = {"link": product_link, "max_price": max_price}
        config["desejos"].append(novo_produto)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'settings.json')

        try:
            with open(file_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            logger.info(f"Link '{product_link}' adicionado à lista de desejos com preço máximo de {max_price}.")
        except Exception as e:
            logger.error(f"Erro ao salvar alterações no arquivo de configuração: {e}")


def get_lista_desejos():
    config = load_config()
    if config is not None and "desejos" in config:
        return config["desejos"]
    else:
        return []


