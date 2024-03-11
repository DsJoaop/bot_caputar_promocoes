from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from src.model.pichau import ProdutoPichau
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PichauScraping:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService(),
                                       options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def _get_soup(self, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    def _extract_img(self, produto: ProdutoPichau) -> str:
        try:
            soup = self._get_soup(produto.link)
            link_img = soup.find('figure', class_='iiz').find('img').get('src')
            return link_img
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou encontrar elementos:", e)

    def create_product(self, link, max_price=None) -> Optional[ProdutoPichau]:
        try:
            soup = self._get_soup(link)
            nome_tag = soup.find('meta', {'property': 'og:title'}).get('content')
            product_price_with_currency = soup.find('meta', {'property': 'product:price:amount'})
            if not product_price_with_currency:
                return None
            product_price = float(product_price_with_currency.get('content').replace('R$', '').replace(',', '').strip())
            product = ProdutoPichau(link, product_price)
            product.category = ' '.join(nome_tag.split()[:3])
            product.link_img = self._extract_img(product)
            product.nome = nome_tag
            product.max_price = max_price
            return product
        except (requests.RequestException, AttributeError) as e:
            print("Falha ao obter a página ou encontrar elementos:", e)
            return None

    def scraping_category(self, url, max_price=None) -> List[ProdutoPichau]:
        try:
            soup = self._get_soup(url)
            cards = soup.find_all(attrs={"data-cy": "list-product"})
            produtos = []
            for card in cards:
                link_produto = f"https://www.pichau.com.br{card.get('href').replace("'", '')}"
                produto = self.create_product(link_produto, max_price)
                if produto is None:
                    break
                print(f"{produto.nome} adicionado")
                produtos.append(produto)
            return produtos
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []

    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        try:
            product_price_with_currency = soup.find('meta', {'property': 'product:price:amount'}).get('content')
            if product_price_with_currency:
                product_price = float(product_price_with_currency.replace('R$', '').replace(',', '').strip())
                return product_price
        except (AttributeError, ValueError) as e:
            print("Falha ao extrair preço:", e)

    def extract_price(self, link, max_price=None) -> Optional[float]:
        try:
            soup = self._get_soup(link)
            return self._extract_price(soup)
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)

    def extract_price_url(self, link, max_price=None) -> Tuple[Optional[float], Optional[str]]:
        try:
            soup = self._get_soup(link)
            price = self._extract_price(soup)
            return price, link
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)

    def value_buy(self, link):
        try:
            self.driver.get(link)
            element = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "td.MuiTableCell-root.MuiTableCell-body[MuiTableCell-alignRight][width='150']")))

            print(f"Valor: {element.text.strip()}")
        except TimeoutException as e:
            print(f"Erro {e}")
        finally:
            self.driver.quit()


def main():
    pichau_scraping = PichauScraping()
    link_produto = "https://www.pichau.com.br/account/orders/1007832083"
    pichau_scraping.value_buy(link_produto)


if __name__ == "__main__":
    main()
