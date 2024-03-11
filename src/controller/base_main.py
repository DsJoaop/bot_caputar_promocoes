import os

from dotenv import load_dotenv

from config.setting_load import load_config
from monitor.pelando.data.data_pelando import PelandoScraping
from monitor.pichau.buy.buy_iteration import PichauAutomator
from monitor.pichau.data.data_pichau import PichauScraping
from src.telegram.notifier import Notifier


class BaseMain:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self._config = load_config()
        self._buy_automation = PichauAutomator()
        self._scraper_pichau = PichauScraping()
        self._scraper_pelando = PelandoScraping()
        self._notificador = Notifier()
        self._config_desejos = self._config['desejos']

    def get_config(self) -> dict:
        return self._config

    def get_config_desejos(self):
        return self._config_desejos

    def get_buy_pichau(self) -> PichauAutomator:
        return self._buy_automation

    def get_bot_token(self) -> str:
        return self._bot_token

    def get_notify(self) -> Notifier:
        return self._notificador

    def get_scraper_pichau(self) -> PichauScraping:
        return self._scraper_pichau

    def get_scraper_pelando(self) -> PelandoScraping:
        return self._scraper_pelando
