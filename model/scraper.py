import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
from produto import Produto

class Scraper:
    def __init__(self, headers):
        self.headers = headers

    def extrair_informacoes_produto(self, card, categoria):
        try:
            link = card.find('a', class_='jss16')['href']
            price_tag = card.find('div', class_='jss88')

            if price_tag:
                price = price_tag.get_text(separator='', strip=True).replace('R$&nbsp;', '').replace(',', '').replace('.', '')
                return Produto(link, price.strip(), categoria)
            else:
                return None
        except AttributeError as e:
            print(f"Erro ao extrair informações do produto: {e}")
            return None

    def fazer_scraping_produtos(self, url, categoria):
        try:
            with requests.Session() as session:
                response = session.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.find_all('div', class_='MuiPaper-root jss284 MuiPaper-elevation1 MuiPaper-rounded')

                informacoes_produto = []
                for card in cards:
                    produto = self.extrair_informacoes_produto(card, categoria)
                    if produto:
                        informacoes_produto.append(produto)

                return informacoes_produto
        except requests.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")
            return None
        except Exception as e:
            print(f"Erro ao fazer scraping: {e}")
            return None