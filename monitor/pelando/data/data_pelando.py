import requests
from bs4 import BeautifulSoup


class PelandoScraping:
    def extact_product(self, card, max_price=None):
        link_element = card.find('a', class_='sc-fzoWTu')
        # Extraia o texto do link (o nome do produto) e o link (o href do elemento <a>)
        nome_produto = link_element.text.strip()
        link_produto = "https://pelando.com.br" + link_element['href']

        response = requests.get(link_produto, headers=self.headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        elemento_span = soup.find('span', {'data-testid': 'deal-stamp', 'class': 'sc-iFQUtD hleQvy sc-dTkguQ fIZFBf'})
        preco = elemento_span.find('span').text.strip()
        try:
            cupom = soup.find('div', 'sc-bCvmQg').text.strip()
        except:
            cupom = None
        float(preco)
        print("Elemento span capturado:")
        print(elemento_span)

    def get_category(self, url, max_price=None):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all("li", "sc-cb8be5d8-2 hliMah")

            product = []
            for card in cards:
                produto = self.extact_product(card, max_price)
                if produto is None:
                    # Se o produto não puder ser extraído, saia do loop
                    break
                product.append(produto)
            return product
        except requests.RequestException as e:
            print("Falha ao obter a página:", e)
            return []

    def extract_img(self, produto):
        return None

    def create_product(self, link, max_price=None):
        return None

    def extract_price(self, link):
        pass


# Exemplo de uso:
if __name__ == "__main__":
    pichau_scraping = PelandoScraping()
    pichau_scraping.get_category("https://www.pelando.com.br/eletronicos")
