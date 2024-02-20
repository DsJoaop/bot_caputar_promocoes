import time
import logging
from typing import List

from src.controller.controller_links import ControllerLinks
from src.model.produto import Produto
from src.telegram.notify import Notificacao


class AnalyzePelando:
    def __init__(self, categoria: str, url: str, controlador_link: ControllerLinks, produtos_desejados: List[Produto],
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
            logging.error(f"Erro ao fazer scraping inicial: {str(e)}")
            return {}

    def enviar_notificacao(self, produto):
        self.notificador.enviar_alerta_nova_promocao(produto)

    def run(self):
        while True:
            start_time = time.time()
            try:
                novos_produtos = self.controlador_link.get_category(self.url)

                for novo_produto in novos_produtos:
                    produto_existente = next((p for p in self.produtos if p.nome == novo_produto.nome), None)
                    if not produto_existente:
                        self.produtos.append(novo_produto)
                        self.enviar_notificacao(novo_produto)


                self.produtos = novos_produtos

            except Exception as e:
                logging.error(f"Erro ao fazer scraping inicial: {str(e)}")

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
