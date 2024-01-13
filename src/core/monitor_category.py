import random
import time
from copy import deepcopy
from src.data_acess.buy_pichau import PichauAutomator
from src.data_acess.scraper.extract_data_pichau import scraping_produtos_pichau, criar_produto_link_pichau


class CategoryMonitor:
    def __init__(self, categoria, url, desconto_minimo, notificador, produtos_desejados):
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.produtos = {}
        self.produtos_desejados = produtos_desejados
        self.automator = PichauAutomator()

        novos_produtos = scraping_produtos_pichau(self.url)
        for produto in novos_produtos:
            self.produtos[produto.link] = produto

    def verificar_desconto_produto_desejado(self, produto, preco_anterior, discount):
        if produto.link in self.produtos_desejados:
            produto_anterior = self.produtos.get(produto.link)
            if produto_anterior and produto.price <= produto_anterior.max_price:
                self.notificador.enviar_compra_confirmada(
                    criar_produto_link_pichau(produto.link),
                    preco_anterior,
                    discount
                )
                self.automator.run_automation_boleto(produto.link)
                return
        self.notificador.enviar_notificacao(
            criar_produto_link_pichau(produto.link), preco_anterior, discount
        )
        self.produtos[produto.link] = produto

    def run(self):
        while True:
            start_time = time.time()
            novos_produtos = scraping_produtos_pichau(self.url)

            produtos_copia = deepcopy(self.produtos)
            for novo_produto in novos_produtos:
                link = novo_produto.link
                if link in produtos_copia:
                    produto_anterior = produtos_copia[link]
                    discount = ((produto_anterior.price - novo_produto.price) / produto_anterior.price) * 100
                    if discount > 0:
                        self.verificar_desconto_produto_desejado(
                            criar_produto_link_pichau(novo_produto.link),
                            produto_anterior.price,
                            discount
                        )
                else:
                    self.notificador.enviar_alerta(
                        criar_produto_link_pichau(novo_produto.link)
                    )
                    self.produtos[link] = novo_produto

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
            time.sleep(random.uniform(30, 100))