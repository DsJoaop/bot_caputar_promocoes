import logging

from src.controller.controller_scraps import ControllerScraps
from src.telegram.notifier import Notifier

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    links = ControllerScraps()
    notificador: Notifier = links.get_notify()
    produto = links.create_product("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                                   "-pch-ps100-24prgbwht")
    preco = links.get_price("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                            "-pch-ps100-24prgbwht")
    notificador.enviar_notificacao_desconto(produto, 50, 30)
