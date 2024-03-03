from typing import List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from src.model.pichau import ProdutoPichau


class PichauScraping:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def scraping_category(self, url, max_price=None) -> List[ProdutoPichau]:
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all(attrs={"data-cy": "list-product"})

            produtos = []
            for card in cards:
                link_produto = card.get('href')
                link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"
                produto = self.create_product(link_produto, max_price)
                preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))
                if produto is None or preco_element is None:
                    # Se o produto não puder ser extraído, saia do loop
                    break
                print(f"{produto.nome} adicionado")
                produtos.append(produto)
            return produtos
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []

    def extract_img(self, produto: ProdutoPichau) -> str:
        try:
            response = requests.get(produto.link, headers=self.headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            link_img = soup.find('figure', class_='iiz').find('img').get('src')
            return link_img
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou en"
                  "contrar elementos:", e)

    def create_product(self, link, max_price=None) -> Optional[ProdutoPichau]:
        try:
            response = requests.get(link, headers=self.headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            nome_tag = soup.find('meta', {'property': 'og:title'}).get('content')

            # Encontrar o preço do produto
            product_price_with_currency = soup.find('meta', {'property': 'product:price:amount'})
            if product_price_with_currency:
                product_price = product_price_with_currency.get('content').replace('R$', '').replace(',', '').strip()
            else:
                return None

            # Criar objeto Produto
            product = ProdutoPichau(response.url, float(product_price))
            product.category = nome_tag.split()[0] + ' ' + nome_tag.split()[1] + ' ' + nome_tag.split()[2]
            product.link_img = self.extract_img(product)
            product.nome = nome_tag
            product.max_price = max_price

            return product
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou encontrar elementos:", e)
            return None

    def extract_price(self, link, max_price=None) -> float:
        try:
            response = requests.get(link, headers=self.headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            product_price_with_currency = soup.find('meta', {'property': 'product:price:amount'}).get('content')

            if product_price_with_currency:
                product_price = product_price_with_currency.replace('R$', '').replace(',', '').strip()
                return float(product_price)
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou encontrar elementos:", e)

    def extract_price_url(self, link, max_price=None) -> tuple[float, str]:
        try:
            response = requests.get(link, headers=self.headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            product_price_with_currency = soup.find('meta', {'property': 'product:price:amount'}).get('content')

            if product_price_with_currency:
                product_price = product_price_with_currency.replace('R$', '').replace(',', '').strip()
                return float(product_price), response.url
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou encontrar elementos:", e)


def main():
    pichau_scraping = PichauScraping()


    # Teste para a função criar_produto
    link_produto = ("https://www.pichau.com.br/processador-amd-ryzen-5-2400g-quad-core-3-6ghz-3-9ghz-turbo-6mb-cache"
                    "-am4-yd2400c5fbbox")
    produto = pichau_scraping.create_product(link_produto)
    if produto:
        print("\nProduto criado:")
        print(produto)


if __name__ == "__main__":
    main()
