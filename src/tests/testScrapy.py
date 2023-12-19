import unittest
from src.data_acess.extractData import Scraper  # Importe a classe Scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes, como os headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.scraper = Scraper(self.headers)

    def test_login(self):
        # Teste de login
        logged_in = self.scraper.fazer_login('joaopaulo.eu29@hotmail.com', 'HLWpichau5566-')
        self.assertTrue(logged_in)  # Verifica se o login foi bem-sucedido

    def test_scraping(self):
        # Teste de scraping após o login
        # Supõe-se que o login foi feito corretamente no teste anterior
        url = 'https://www.pichau.com.br/account/orders'  # URL de teste para scraping
        categoria = 'categoria_de_teste'  # Categoria fictícia para o teste

        # Teste se o scraping é bem-sucedido após o login
        produtos = self.scraper.fazer_scraping_produtos(url, categoria)
        self.assertIsNotNone(produtos)  # Verifica se a lista de produtos não está vazia

if __name__ == '__main__':
    unittest.main()
