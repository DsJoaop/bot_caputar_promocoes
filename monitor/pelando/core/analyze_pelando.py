import time
import logging
from typing import List

from src.model.oferta import Oferta
from src.controller.controller_scraps import ControllerScraps
from src.model.desconto import Desconto
from src.telegram.notify import Notificacao


class AnalyzePelando:
    def __init__(self, categoria: str, url: str, controlador_link: ControllerScraps, produtos_desejados: List[Desconto],
                 notificador):
        self.controlador_link = controlador_link
        self.categoria = categoria
        self.url = url
        self.notificador: Notificacao = notificador
        self.produtos_desejados = produtos_desejados
        self.produtos = self._scraping_inicial()

    def _scraping_inicial(self):
        try:
            novos_produtos = self.controlador_link.get_category(self.url)
            return novos_produtos
        except Exception as e:
            logging.error(f"Erro ao fazer o primeiro scraping: {str(e)}")
            return {}

    def enviar_notificacao(self, produto: Oferta):
        self.notificador.enviar_alerta_nova_promocao(produto)

    def run(self):
        while True:
            start_time = time.time()
            try:
                novas_ofertas: List[Oferta] = self.controlador_link.get_category(self.url)

                for oferta in novas_ofertas:
                    produto_existente = next((p for p in self.produtos if p.id == oferta.id), None)
                    if not produto_existente:
                        self.produtos.append(oferta)
                        self.enviar_notificacao(oferta)

                self.produtos = novas_ofertas

            except Exception as e:
                logging.error(f"Erro ao fazer scraping inicial: {str(e)}")

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")

