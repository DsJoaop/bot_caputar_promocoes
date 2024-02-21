import logging

from src.controller.controller_scraps import ControllerScraps
from src.telegram.notify import Notificacao

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    links = ControllerScraps()
    notificador: Notificacao = links.get_notify()
    produto = links.create_product("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                                   "-pch-ps100-24prgbwht")
    preco = links.get_price("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                            "-pch-ps100-24prgbwht")
    notificador.enviar_notificacao_desconto(produto, 50, 30)
