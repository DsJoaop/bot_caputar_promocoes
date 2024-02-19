import random
import time
import logging
import threading
from typing import List

from src.controller.controller_links import ControllerLinks
from src.model.produto import Produto
from monitor.pichau.buy.buy_pichau import PichauAutomator
from src.telegram.notify import Notificacao


class AnalyzePichau:
    def __init__(self, categoria: str, url: str, controlador_link: ControllerLinks, produtos_desejados: List[Produto],
                 notificador):
        self.controlador_link = controlador_link
        self.categoria = categoria
        self.url = url
        self.notificador: Notificacao = notificador
        self.produtos_desejados = produtos_desejados
        self.automator = PichauAutomator()
        self.produtos = self._scraping_inicial()

    def _scraping_inicial(self):
        try:
            novos_produtos = self.controlador_link.get_category(self.url)
            return novos_produtos
        except Exception as e:
            logging.error(f"Erro ao fazer scraping inicial: {str(e)}")
            return {}

    def _verificar_desconto_produto_desejado(self, produto, novo_preco, preco_anterior, discount, indice):
        try:
            if discount > 0:
                self.notificador.enviar_notificacao(
                    produto, preco_anterior, discount, novo_preco
                )
                for produto_desejado in self.produtos_desejados:
                    if produto.link == produto_desejado.link:
                        self.automator.run_automation_boleto(produto.link)
                        break
                self.produtos[indice].price = novo_preco
        except Exception as e:
            logging.error(f"Erro ao verificar desconto do produto: {str(e)}")

    def _check_price(self, produto_atual, indice):
        time.sleep(random.uniform(1, 40))
        try:
            novo_preco = self.controlador_link.get_price_pichau(produto_atual.link)
            if produto_atual.price > novo_preco:
                discount = ((novo_preco - produto_atual.price) / novo_preco) * 100
                if abs(discount) >= 1:  # Considera mudanças de preço significativas
                    self._verificar_desconto_produto_desejado(
                        produto_atual,
                        novo_preco,
                        produto_atual.price,
                        discount,
                        indice
                    )
                    # Atualiza o produto na lista de produtos
                    self.produtos[indice].price = novo_preco
        except Exception as e:
            logging.error(f"Erro ao verificar o preço do produto: {str(e)}")

    def run(self):
        while True:
            start_time = time.time()
            try:
                threads = []
                for indice, produto_atual in enumerate(self.produtos):
                    thread = threading.Thread(target=self._check_price, args=(produto_atual, indice))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            except Exception as e:
                logging.error(f"Erro durante a execução: {str(e)}")

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
