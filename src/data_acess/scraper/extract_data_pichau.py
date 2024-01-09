import requests
from bs4 import BeautifulSoup
from src.model.produto_completo import Produto
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def extrair_card_completo(card, max_price=None):
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
        produto = Produto(link_produto, valor_float, categoria, nome, None, max_price)
        return produto
    return None


def extrair_card_simples(card, max_price=None):
    link_produto = card.get('href')
    preco_element = card.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))
    if preco_element:
        valor_texto = preco_element.get_text().strip()
        valor_sem_RS = re.sub(r'[^\d.]', '', valor_texto)
        link_produto = f"https://www.pichau.com.br{link_produto.replace("'", '')}"
        return Produto(link_produto, float(valor_sem_RS))
    return None


def scraping_produtos_pichau(url, extrair_informacao=extrair_card_simples, max_price=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all(attrs={"data-cy": "list-product"})

        produtos = []
        for card in cards:
            produto = extrair_informacao(card,max_price)
            if produto is None:
                # Se o produto não puder ser extraído, saia do loop
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
        produto.link_img = "https://salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"


def criar_produto_link_pichau(link, max_price=None):
    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tente encontrar os elementos e obtenha os atributos
        link_img = soup.find('figure', class_='iiz').find('img').get('src')
        nome = soup.find('figure', class_='iiz').find('img').get('alt')
        preco_element = soup.find(lambda tag: tag.name == 'div' and tag.get_text().strip().startswith('R$'))

        if preco_element:
            valor_texto = preco_element.get_text().strip()
            valor_sem_RS = re.sub(r'[^\d.]', '', valor_texto)
            link_produto = link
            categoria = nome.split()[0] + ' ' + nome.split()[1] + ' ' + nome.split()[2]
            return Produto(link_produto, float(valor_sem_RS), categoria, nome, link_img, max_price)

    except (requests.RequestException, AttributeError) as e:
        print("Falha ao obter a página ou encontrar elementos:", e)
        return None


def listar_produtos(links):
    produtos = []
    for link in links:
        produto = criar_produto_link_pichau(link['link'], link['max_price'])
        if produto:
            produtos.append(produto)
        else:
            produtos.extend(scraping_produtos_pichau(link['link'], extrair_card_completo, link['max_price']))

    return produtos


def formatar_mensagem(produtos):
    mensagem = "<b>🛒 Produtos Desejados (Serão comprados automáticamente 🤖)</b>\n\n"
    for produto in produtos:
        mensagem += f"<b>Nome:</b> <a href='{produto.link}'>{produto.nome[:57]}...</a>\n"
        mensagem += f"🔹 <b>Categoria:</b> {produto.category}\n"
        mensagem += f"💰 <b>Preço:</b> R$ {produto.price}\n\n"
    return mensagem
