import os
from typing import List

from dotenv import load_dotenv

from config.setting_load import load_config
from src.controller.controller_scraps import ControllerScraps
from src.model.desconto import Desconto
from monitor.pichau.buy.buy_pichau import PichauAutomatorOld
from src.telegram.notifier import Notifier


class BaseMain:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self._config = load_config()
        self._buy_automation = PichauAutomatorOld()
        self._product_link = ControllerScraps()
        self._notificador = Notifier()
        self._config_desejos = self._config['desejos']

    def get_config(self) -> dict:
        return self._config

    def get_config_desejos(self):
        return self._config_desejos

    def get_buy_pichau(self) -> PichauAutomatorOld:
        return self._buy_automation

    def get_bot_token(self) -> str:
        return self._bot_token

    def get_products(self) -> List[Desconto]:
        return self._product_link.get_list_desejos()

    def get_notify(self) -> Notifier:
        return self._notificador

    def get_controller_links(self) -> ControllerScraps:
        return self._product_link



