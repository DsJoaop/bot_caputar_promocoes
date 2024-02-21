from typing import List

from config.setting_load import load_config
from src.controller.controller_scraps import ControllerScraps
from src.model.desconto import Desconto
from monitor.pichau.buy.buy_pichau import PichauAutomator
from src.telegram.notify import Notificacao


class BaseMain:
    def __init__(self):
        self._config = load_config()
        self._config_telegram = self._config['telegram']
        self._config_desejos = self._config['desejos']
        self._bot_token = self._config_telegram['bot_token']
        self._buy_automation = PichauAutomator()
        self._product_link = ControllerScraps()
        self._notificador = Notificacao()

    def get_config(self) -> dict:
        return self._config

    def get_config_telegram(self):
        return self._config_telegram

    def get_config_desejos(self):
        return self._config_desejos

    def get_buy_pichau(self) -> PichauAutomator:
        return self._buy_automation

    def get_bot_token(self) -> str:
        return self._bot_token

    def get_products(self) -> List[Desconto]:
        return self._product_link.get_list_desejos()

    def get_notify(self) -> Notificacao:
        return self._notificador

    def get_controller_links(self) -> ControllerScraps:
        return self._product_link



