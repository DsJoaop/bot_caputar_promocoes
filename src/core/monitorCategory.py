import random
import time

from src.data_acess.extractPay import PichauAutomator


class CategoryMonitor:
    def __init__(self, categoria, url, desconto_minimo, notificador, scraper):
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.scraper = scraper
        self.produtos_precos = {}
        self.produtos_notificados = set()
        self.produtos_comprados = set()

    def enviar_notificacao(self, produto, previous_price, current_price, discount):
        if produto.link not in self.produtos_notificados:
            mensagem = (
                f"🎉 Desconto detectado! 🎉\n\n\n"
                f"🔗 Link: {produto.link}\n\n"
                f"💰 Preço anterior: R${previous_price:.2f}\n\n"
                f"💸 Novo preço: R${current_price:.2f}\n\n"
                f"💲 Desconto: {discount:.2f}% OFF\n\n"
                f"\n\n\n\n"
            )
            self.notificador.enviar_mensagem(mensagem)
            print(f"Produto encontrado!!!\n\n {mensagem}")
            self.produtos_notificados.add(produto.link)

    def realizar_compra(self, produto):
        if produto.link not in self.produtos_comprados:
            automator = PichauAutomator()
            automator.run_automation(produto.link)
            self.produtos_comprados.add(produto.link)

    def run(self):
        while True:
            produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)
            if produtos:
                for produto in produtos:
                    previous_price = self.produtos_precos.get(produto.link)
                    if previous_price is not None and produto.price < previous_price:
                        discount = ((previous_price - produto.price) / previous_price) * 100
                        if discount >= self.desconto_minimo:
                            self.enviar_notificacao(produto, previous_price, produto.price, discount)
                            self.realizar_compra(produto)
                # Atualiza a lista de produtos inteira após o scraping
                self.produtos_precos = {produto.link: produto.price for produto in produtos}
            else:
                print(f"Nenhum produto encontrado para a categoria: {self.categoria}")
            print(f"Analisando {self.categoria}...")
            time.sleep(random.uniform(60, 200))