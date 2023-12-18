import requests
from bs4 import BeautifulSoup
import re
from src.model.produto import Produto


class Scraper:
    def __init__(self, headers):
        self.headers = headers

    def extrair_informacoes_produto(self, card, categoria):
        link_produto = card.get('href')
        preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))

        preco_texto = preco_element.get_text().strip() if preco_element else ''
        preco_regex = r'R\$\s?(\d{1,3}(?:[.,]\d{3})*(?:,\d{1,2})?)'

        preco_match = re.search(preco_regex, preco_texto)

        if preco_match:
            preco_formatado = preco_match.group(1).replace('.', '').replace(',', '.')
            preco_produto = float(preco_formatado)
            link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"
            return Produto(link_produto, preco_produto, categoria)

        return None

    def fazer_scraping_produtos(self, url, categoria):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)  # Reduzindo o timeout para 10 segundos
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all(attrs={"data-cy": "list-product"})

            produtos = [self.extrair_informacoes_produto(card, categoria) for card in cards]
            return [produto for produto in produtos if produto]
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []