import requests
from bs4 import BeautifulSoup
from src.model.produto import Produto

class Scraper:
    def __init__(self, headers):
        self.headers = headers

    def extrair_informacoes_produto(self, card, categoria):
        # Extrair informações do card, como link e preço
        link_produto = card.get('href')
        preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))

        # Se o elemento do preço for encontrado
        if preco_element:
            preco_texto = preco_element.get_text().strip()

            # Convertendo o preço para float
            preco_produto = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.'))

            # Modificar o link conforme especificado
            link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"

            # Aqui você pode criar um objeto Produto ou imprimir os dados obtidos
            produto = Produto(link_produto, preco_produto, categoria)
            return produto
        else:
            # Caso não encontre informações de preço para este card
            return None

    def fazer_scraping_produtos(self, url, categoria):
        # Fazer a requisição GET
        response = requests.get(url, headers=self.headers)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar todos os elementos com o atributo data-cy="list-product"
            cards = soup.find_all(attrs={"data-cy": "list-product"})

            # Iterar sobre os cards e extrair as informações de cada produto
            produtos = []
            for card in cards:
                produto = self.extrair_informacoes_produto(card, categoria)
                if produto:
                    produtos.append(produto)

            return produtos
        else:
            print("Falha ao obter a página:", response.status_code)
            return None
