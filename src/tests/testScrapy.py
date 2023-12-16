import unittest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.data_acess.scraper import Scraper



class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        self.url = 'https://www.pichau.com.br/hardware/memorias'
        self.categoria = 'Memórias'

    def test_fazer_scraping_produtos(self):
        try:
            # Chama o método fazer_scraping_produtos
            produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)

            # Verifica o status da resposta HTTP
            response = requests.get(self.url, headers=self.scraper.headers)
            print(f'Código de status da requisição: {response.status_code}')

            # Verifica se a lista de produtos não está vazia
            self.assertIsNotNone(produtos)

            # Verifica se os produtos possuem as informações esperadas
            for produto in produtos:
                self.assertIsNotNone(produto.link)
                self.assertIsNotNone(produto.price)
                self.assertIsNotNone(produto.category)
                self.assertEqual(produto.category, self.categoria)

            # Imprime a lista de produtos no console
            if produtos:
                print("Lista de produtos:")
                for produto in produtos:
                    print(f"Link: {produto.link}, Preço: {produto.price}, Categoria: {produto.category}")
            else:
                print("Nenhum produto encontrado.")
        except requests.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Conteúdo da resposta: {e.response.text}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


if __name__ == '__main__':
    unittest.main()
