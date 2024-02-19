from typing import List

from config.setting_load import get_lista_desejos
from monitor.pelando.data.data_pelando import PelandoScraping
from monitor.pichau.data.data_pichau import PichauScraping
from src.model.produto import Produto
from monitor.pichau.buy.buy_pichau import PichauAutomator


class ControllerLinks:
    def __init__(self, headers=None):
        self._pichau = PichauScraping()
        self._pelando = PelandoScraping()
        self._buy_pichau = PichauAutomator()

    def get_category(self, link: str, max_price=None) -> List[Produto]:
        if 'pichau.com.br' in link:
            return self._pichau.scraping_category(link, max_price)
        elif 'pelando.com' in link:
            return self._pelando.get_category(link, max_price)

    def get_list_desejos(self) -> List[Produto]:
        desejos = get_lista_desejos()
        produtos = []
        for link_info in desejos:
            link = link_info['link']
            max_price = link_info['max_price']
            if 'pichau.com.br' in link:
                produto = self._pichau.create_product(link, max_price)
                if produto:
                    produtos.append(produto)
                else:
                    produtos.extend(self._pichau.scraping_category(link))
            elif 'pelando.com.br' in link:
                produto = self._pelando.create_product(link)
                if produto:
                    produtos.append(produto)
                else:
                    produtos.extend(self._pelando.get_category(link, max_price))
        return produtos

    def create_product(self, link: str) -> Produto:
        if 'pichau.com.br' in link:
            return self._pichau.create_product(link)
        elif 'pelando.com' in link:
            return self._pelando.create_product(link)

    def get_price(self, link) -> float:
        if 'pichau.com.br' in link:
            return self._pichau.extract_price(link)
        elif 'pelando.com' in link:
            return self._pelando.extract_price(link)

    def get_price_pichau(self, link) -> float:
        return self._pichau.extract_price(link)