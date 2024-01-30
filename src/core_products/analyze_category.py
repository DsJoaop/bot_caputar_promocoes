import time

from src.data_acess.data_pichau import scraping_produtos_pichau, criar_produto_link_pichau
from src.share.buy_pichau.buy_pichau import PichauAutomator


class AnalyzeCategory:
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
        start_time = time.time()

        # Perform scraping and obtain the latest products
        novos_produtos = scraping_produtos_pichau(self.url)

        i = 0
        # Check for new products and add them to the existing ones
        for novo_produto in novos_produtos:
            link = novo_produto.link
            if link not in self.produtos and i > 0:
                self.produtos[link] = novo_produto
                self.notificador.enviar_alerta(criar_produto_link_pichau(link))
        i += 1
        # Iterate through all products and check for price drops
        for produto_link, produto in self.produtos.items():
            produto_anterior = self.produtos.get(produto_link)
            if produto_anterior and produto.price < produto_anterior.price:
                discount = ((produto_anterior.price - produto.price) / produto_anterior.price) * 100
                self.verificar_desconto_produto_desejado(
                    criar_produto_link_pichau(produto.link),
                    produto_anterior.price,
                    discount
                )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
        time.sleep(1)
