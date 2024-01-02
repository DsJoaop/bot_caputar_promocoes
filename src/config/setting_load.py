import json
import logging
import os

from src.data_acess.scraper.extract_data_pichau import listar_produtos, formatar_mensagem
from src.telegram.telegram_mensages import send_mensage

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


def add_produto_desejo(product_link):
    config = load_config()
    if config is not None:
        if "desejos" not in config:
            config["desejos"] = []

        config["desejos"].append(product_link)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'settings.json')

        try:
            with open(file_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            logger.info(f"Link '{product_link}' adicionado à lista de desejos.")
        except Exception as e:
            logger.error(f"Erro ao salvar alterações no arquivo de configuração: {e}")


def get_lista_desejos():
    config = load_config()
    if config is not None and "desejos" in config:
        return config["desejos"]
    else:
        return []


def main():
    # Adicionando produtos à lista de desejos
    add_produto_desejo("https://www.pichau.com.br/cadeira-office-zinnia-zurich-preto-zno-zrc-bk")
    add_produto_desejo("https://www.pichau.com.br/monitor-gamer-pichau-cepheus-fuse-vpro49-ultra-49-pol-nano-ips-2k-1ms-144hz-freesync-hdmi-dp-pg-cfvfs49u-bl01")
    links = get_lista_desejos()
    if links is not None:
        produtos = listar_produtos(links)
        send_mensage(formatar_mensagem(produtos))
    else:
        send_mensage("Erro ao carregar lista de desejo")


if __name__ == "__main__":
    main()
