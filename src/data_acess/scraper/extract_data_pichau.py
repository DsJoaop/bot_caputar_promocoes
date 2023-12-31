import requests
from bs4 import BeautifulSoup
from src.model.produto import Produto
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def extrair_cards(card):
    link_produto = card.get('href')
    preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))
    nome_tag = card.find('h2', class_='MuiTypography-root')
    if preco_element:
        valor_texto = preco_element.get_text().strip()
        valor_sem_RS = re.sub(r'[^\d.]', '', valor_texto)
        # Converter para float
        valor_float = float(valor_sem_RS)
        link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"
        nome = nome_tag.get_text()
        categoria = nome.split()[0] + ' ' + nome.split()[1] + ' ' + nome.split()[2]
        return Produto(link_produto, valor_float, categoria, nome)

    return None


def scraping_produtos_pichau(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all(attrs={"data-cy": "list-product"})

        produtos = []
        for card in cards:
            produto = extrair_cards(card)
            if produto is None:
                # Se o product não puder ser extraído, saia do loop
                break
            produtos.append(produto)
        return produtos
    except requests.RequestException as e:
        print("Falha ao obter a página:", e)
        return []


def extrair_imagem_produto_pichau(produto):
    try:
        response = requests.get(produto.link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        produto.link_img = soup.find('figure', class_='iiz').find('img').get('src')

    except requests.RequestException as e:
        print("Falha ao obter a página:", e)


def criar_produto_link(link):
    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        link_img = soup.find('figure', class_='iiz').find('img').get('src')
        nome = soup.find('figure', class_='iiz').find('img').get('alt')

        preco_element = soup.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))

        if preco_element:
            valor_texto = preco_element.get_text().strip()
            valor_sem_RS = re.sub(r'[^\d.]', '', valor_texto)
            # Converter para float
            valor_float = float(valor_sem_RS)
            link_produto = link
            categoria = nome.split()[0] + ' ' + nome.split()[1]+ ' ' + nome.split()[2]
            return Produto(link_produto, valor_float, categoria, link_img, nome)

    except requests.RequestException as e:
        print("Falha ao obter a página:", e)
