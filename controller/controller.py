import logging
import time
from model import Scraper
from view import Notificacao, Logger
from config import Config

class Controller:
    def __init__(self):
        self.logger = Logger(__name__)
        self.config = Config()
        self.scraper = Scraper({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        self.notificacao = Notificacao()

    def monitorar_precos(self, listURLs_categorias, intervalo=60):
        precos_antigos = {categoria: [] for categoria in listURLs_categorias}

        while True:
            for categoria, url in listURLs_categorias.items():
                preco_novo = self.scraper.fazer_scraping_produtos(url, categoria)

                if preco_novo:
                    preco_antigo = precos_antigos[categoria]
                    if preco_antigo:
                        precos_antigos[categoria] = self.scraper.comparar_precos(preco_antigo, preco_novo)
                    else:
                        precos_antigos[categoria] = preco_novo

            time.sleep(intervalo)


    def main(self):
        config_data = self.config.load_config()

        if config_data:
            telegram_config = config_data.get('telegram', {})
            bot_token = telegram_config.get('bot_token')
            chat_id = telegram_config.get('chat_id')

            if bot_token and chat_id:
                listURLs_categorias = config_data.get('categorias', {})
                self.monitorar_precos(listURLs_categorias)
            else:
                self.logger.log_error("Configurações do Telegram incompletas. Verifique o arquivo de configuração.")
        else:
            self.logger.log_error("Falha ao carregar configurações.")


#Iniciando o controlador
if __name__ == "__main__":
    controller = Controller()
    controller.main()
