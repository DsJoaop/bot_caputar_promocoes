import time

import requests
from bs4 import BeautifulSoup
from src.model.produto import Produto
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def extrair_informacoes_produto(card, categoria):
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


def fazer_scraping_produtos(url, categoria):
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all(attrs={"data-cy": "list-product"})

        produtos = []
        for card in cards:
            produto = extrair_informacoes_produto(card, categoria)
            if produto is None:
                # Se o product não puder ser extraído, saia do loop
                break
            produtos.append(produto)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tempo de extração: {execution_time:.4f} segundos")
        return produtos
    except requests.RequestException as e:
        print("Falha ao obter a página:", e)
        return []


def extrair_informacao_produto_especifico(produto):
    try:
        response = requests.get(produto.link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Supondo que 'product' já está instanciado como um objeto da classe Produto
        produto.link_img = soup.find('figure', class_='iiz').find('img').get('src')
        produto.nome = soup.find('figure', class_='iiz').find('img').get('alt')

    except requests.RequestException as e:
        print("Falha ao obter a página:", e)
