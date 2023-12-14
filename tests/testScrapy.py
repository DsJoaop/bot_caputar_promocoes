import unittest
from scraper import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        self.url = 'https://www.pichau.com.br/hardware/placa-m-e'
        self.categoria = 'Placas Mãe'

    def test_fazer_scraping_produtos(self):
        # Chama o método fazer_scraping_produtos
        produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)

        # Verifica se a lista de produtos não está vazia
        self.assertIsNotNone(produtos)
        
        # Verifica se os produtos possuem as informações esperadas
        for produto in produtos:
            self.assertIsNotNone(produto.link)
            self.assertIsNotNone(produto.price)
            self.assertIsNotNone(produto.category)
            self.assertEqual(produto.category, self.categoria)

if __name__ == '__main__':
    unittest.main()
