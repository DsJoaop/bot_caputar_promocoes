import logging

from src.controller.controller_links import ControllerLinks
from src.telegram.notify import Notificacao

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    links = ControllerLinks()
    notificador: Notificacao = links.get_notify()
    produto = links.create_product("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                                   "-pch-ps100-24prgbwht")
    preco = links.get_price("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                            "-pch-ps100-24prgbwht")
    notificador.enviar_notificacao(produto, 50, 30)
