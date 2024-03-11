import logging
from typing import List

import requests
from bs4 import BeautifulSoup

from src.model.oferta import Oferta
from src.model.cupom import Cupom
from src.model.desconto import Desconto
from src.model.gratis import Gratis


def _extract_info(soup, link, oferta_type, codigo=None, categoria=None) -> Oferta:
    titulo = soup.find('title').text.strip().rstrip(" | Pelando")
    image = soup.find('meta', {'property': 'og:image'})['content']
    loja = soup.find('a', class_='sc-jGnTwx').text.strip()
    id_oferta = titulo

    if oferta_type == 'gratis':
        return Oferta(identificador=id_oferta, gratis=Gratis(link, loja, titulo, image))
    elif oferta_type == 'cupom':
        desconto = soup.find('span', {'data-testid': 'deal-stamp'}).find('span').text.strip()
        return Oferta(identificador=id_oferta, cupom=Cupom(link, image, loja, titulo, codigo, desconto))
    else:
        preco = soup.find('span', {'data-testid': 'deal-stamp'}).find('span').text.strip().replace(',', '.').strip()
        try:
            cupom = soup.find('div', 'sc-bCvmQg').text.strip()
        except AttributeError:
            cupom = None
        return Oferta(identificador=id_oferta, desconto=Desconto(link, float(preco), categoria,
                                                                 loja, titulo, image, cupom))


class PelandoScraping:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def _extract_data(self, link) -> BeautifulSoup:
        response = requests.get(link, headers=self.headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    def create_product(self, link, categoria=None):
        try:
            soup = self._extract_data(link)
            cupom = soup.find('span', string='Pegar cupom')
            element = soup.find('a', href=lambda href: href and href.startswith("https://www.pelando.com.br"))
            span_element = soup.find('span', {'data-masked': True})
            g = soup.find('span', {'data-testid': 'deal-stamp'}).find_all('span')[-1]

            if cupom:
                return _extract_info(soup, link, 'cupom', categoria=categoria)
            elif element and span_element:
                return _extract_info(soup, link, 'cupom', codigo=span_element['data-masked'], categoria=categoria)
            elif 'Grátis' in g:
                return _extract_info(soup, link, 'gratis', categoria=categoria)
            else:
                return _extract_info(soup, link, 'product', categoria=categoria)
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer scraping do produto: {str(e)}", categoria)
            return None

    def scraping_category(self, url, categoria=None) -> List[Oferta]:
        try:
            soup = self._extract_data(url)
            cards = soup.find_all("li", "sc-cb8be5d8-2 hliMah")
            del cards[8]
            products = []

            for card in cards:
                link = "https://pelando.com.br" + card.find_all('a')[1]['href']
                product = self.create_product(link, categoria)
                if product is None:
                    break
                products.append(product)

            return products
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer o primeiro scraping: {str(e)}")

    def scraping_last_item(self, url, max_price=None) -> Oferta:
        try:
            soup = self._extract_data(url)
            cards = soup.find_all("li", "sc-cb8be5d8-2 hliMah")

            link = "https://pelando.com.br" + cards[0].find_all('a')[1]['href']
            product = self.create_product(link, max_price)
            if product is not None:
                return product
            else:
                link = "https://pelando.com.br" + cards[1].find_all('a')[1]['href']
                return self.create_product(link, max_price)
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer o primeiro scraping: {str(e)}")

    def extract_img(self, link):
        try:
            soup = self._extract_data(link)
            return soup.find('meta', {'property': 'og:image'})['content']
        except Exception as e:
            logging.error(f"Erro ao extrair imagem: {str(e)}")
            return None

    def extract_price(self, link):
        try:
            soup = self._extract_data(link)
            return soup.find('span', {'data-testid': 'deal-stamp'}).find('span').text.strip()
        except Exception as e:
            logging.error(f"Erro ao extrair preço: {str(e)}")
            return None


if __name__ == "__main__":
    pelando_scraping = PelandoScraping()
    gratis = pelando_scraping.create_product(
        "https://www.pelando.com.br/d/d4b22942-508f-482c-9b3b-c3bcda464b94/e-book-o-livro-mais-doce-do-mundo-or"
        "-receitas-nestle")
    cupom_na_loja = pelando_scraping.create_product(
        "https://www.pelando.com.br/d/6de0f58b-2d57-4c7c-8b43-70f93fab98ca/rdollar40-off-nas-compras-acima-de"
        "-rdollar199-em-automoveis-e-motocicletas-com-cupom-shopee?expired_deal=true")
    cupom_desconto = pelando_scraping.create_product(
        "https://www.pelando.com.br/d/920eb2d6-3fad-4295-8ce1-2233b91d8bd7/rdollar50-off-em-compras-acima-de"
        "-rdollar250-com-cupom-mercado-carrefour")
    produto4 = pelando_scraping.create_product(
        "https://www.pelando.com.br/d/d4e1259a-1f0f-42d5-a1fd-236406c47d6c/estante-livreiro-5-prateleiras-monza-viero")
    print(str(gratis))
    print(str(cupom_na_loja))
    print(str(cupom_desconto))
    print(str(produto4))
