from typing import List

import requests
from bs4 import BeautifulSoup

from src.model.produto import Produto


class PelandoScraping:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def create_product(self, link, max_price=None):

        response = requests.get(link, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        nome = soup.find('title').text.strip().split(":")[1].split("|")[0]

        image = soup.find('meta', {'property': 'og:image'})['content']
        preco = soup.find('span', {'data-testid': 'deal-stamp'}).find('span').text.strip()
        loja = soup.find('a', class_='sc-jGnTwx').text.strip()

        try:
            cupom = soup.find('div', 'sc-bCvmQg').text.strip()
        except:
            cupom = None

        categoria = nome.split()[0] + ' ' + nome.split()[1] + ' ' + nome.split()[2]
        return Produto(link, preco, categoria, loja, nome, image, max_price, cupom)

    def scraping_category(self, url, max_price=None):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all("li", "sc-cb8be5d8-2 hliMah")
            del cards[8]
            product = []
            for card in cards:
                link = "https://pelando.com.br" + card.find_all('a')[1]['href']
                produto = self.create_product(link, max_price)
                if produto is None:
                    # Se o produto não puder ser extraído, saia do loop
                    break
                product.append(produto)
            return product
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []

    def extract_img(self, link):
        response = requests.get(link, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        image = soup.find('meta', {'property': 'og:image'})['content']
        return image

    def extract_price(self, link):
        response = requests.get(link, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('span', {'data-testid': 'deal-stamp'}).find('span').text.strip()


# Exemplo de uso:
if __name__ == "__main__":
    pichau_scraping = PelandoScraping()
    produtos: List[Produto] = pichau_scraping.scraping_category("https://www.pelando.com.br/eletronicos")
    for produto in produtos:
        print(produto.nome)