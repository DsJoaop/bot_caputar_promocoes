import requests
from bs4 import BeautifulSoup
from src.model.produto import Produto
import re


class Scraper:
    def __init__(self, headers):
        self.headers = headers

    def extrair_informacoes_produto(self, card, categoria):
        link_produto = card.get('href')
        preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))

        if preco_element:
            valor_texto = preco_element.get_text().strip()
            valor_sem_RS = re.sub(r'[^\d.]', '', valor_texto)

            # Converter para float
            valor_float = float(valor_sem_RS)
            link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"
            return Produto(link_produto, valor_float, categoria)

        return None

    def fazer_scraping_produtos(self, url, categoria):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all(attrs={"data-cy": "list-product"})

            produtos = []
            for card in cards:
                produto = self.extrair_informacoes_produto(card, categoria)
                if produto is None:
                    # Se o produto não puder ser extraído, saia do loop
                    break
                produtos.append(produto)

            return produtos
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []
