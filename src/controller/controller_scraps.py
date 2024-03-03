from config.setting_load import get_lista_desejos
from monitor.pelando.data.data_pelando import PelandoScraping
from monitor.pichau.data.data_pichau import PichauScraping
from monitor.pichau.buy.buy_pichau import PichauAutomatorOld
from src.model.oferta import Oferta


class ControllerScraps:
    def __init__(self, headers=None):
        self._pichau = PichauScraping()
        self._pelando = PelandoScraping()
        self._buy_pichau = PichauAutomatorOld()

    def get_category(self, link: str, categoria=None, max_price=None):
        if 'pichau.com.br' in link:
            return self._pichau.scraping_category(link, max_price)
        elif 'pelando.com' in link:
            return self._pelando.scraping_category(link, categoria)

    def get_list_desejos(self):
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
                    produtos.extend(self._pelando.scraping_category(link, max_price))
        return produtos

    def create_product(self, link: str):
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

    def get_last_product(self, link, categoria) -> Oferta:
        return self._pelando.scraping_last_item(link, categoria)
