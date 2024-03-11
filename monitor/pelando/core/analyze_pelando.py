import random
import time
import logging

from monitor.pelando.data.data_pelando import PelandoScraping
from src.model.oferta import Oferta
from src.telegram.notifier import Notifier


class AnalyzePelando:
    def __init__(self, categoria: str, url: str, controlador_link: PelandoScraping, notificador):
        self.controlador_link = controlador_link
        self.categoria = categoria
        self.url = url
        self.notificador: Notifier = notificador
        self.produto = None

    def _scraping_inicial(self):
        try:
            produto = self.controlador_link.scraping_last_item(self.url, self.categoria)
            return produto
        except Exception as e:
            logging.error(f"Erro ao fazer o primeiro scraping: {str(e)}")
            return None

    def enviar_notificacao(self, produto: Oferta):
        self.notificador.enviar_alerta_nova_promocao(produto)

    def run(self):
        while True:
            start_time = time.time()
            try:
                novo_produto: Oferta = self.controlador_link.scraping_last_item(self.url, self.categoria)

                if self.produto is None:
                    self.produto = novo_produto
                elif self.produto.id != novo_produto.id:
                    self.produto = novo_produto
                    self.enviar_notificacao(novo_produto)

            except Exception as e:
                logging.error(f"Erro ao fazer scraping inicial: {str(e)}")

            time.sleep(random.uniform(5, 10))
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
