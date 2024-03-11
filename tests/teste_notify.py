import logging

from monitor.pichau.data.data_pichau import PichauScraping
from src.telegram.notifier import Notifier

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    links = PichauScraping()
    produto = links.create_product("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                                   "-pch-ps100-24prgbwht")
    preco = links.extract_price("https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
                                "-pch-ps100-24prgbwht")
    notificardor = Notifier()
    notificardor.enviar_notificacao_desconto(produto, 50, 30, preco)
