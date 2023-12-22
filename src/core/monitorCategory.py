import concurrent.futures  # For concurrent operations
import time

from src.data_acess.extractPay import PichauAutomator


class CategoryMonitor:
    def __init__(self, categoria, url, desconto_minimo, notificador, scraper):
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.scraper = scraper
        self.automator = PichauAutomator()
        self.produtos = {}  # Dicionário para armazenar link: objeto Produto

        # Primeira execução para definir produtos iniciais
        novos_produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)
        for produto in novos_produtos:
            self.produtos[produto.link] = produto

    def enviar_notificacao(self, produto, previous_price, current_price, discount):
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

    def check_price_changes(self, link, produto_atualizado):
        if link in self.produtos:
            produto_anterior = self.produtos[link]
            previous_price = produto_anterior.price
            current_price = produto_atualizado.price

            if current_price < (1 - self.desconto_minimo / 100) * previous_price:
                discount = ((previous_price - current_price) / previous_price) * 100
                self.automator.run_automation(link)
                self.enviar_notificacao(produto_atualizado, previous_price, current_price, discount)

    def run(self):
        while True:
            start_time = time.time()

            novos_produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)

            for novo_produto in novos_produtos:
                link = novo_produto.link
                if link in self.produtos:
                    produto_anterior = self.produtos[link]
                    previous_price = produto_anterior.price
                    current_price = novo_produto.price

                    if current_price < (1 - self.desconto_minimo / 100) * previous_price:
                        discount = ((previous_price - current_price) / previous_price) * 100
                        self.automator.run_automation(link)
                        self.enviar_notificacao(novo_produto, previous_price, current_price, discount)
                        self.produtos[link] = novo_produto
                else:
                    # Se o produto é novo, adiciona ao dicionário
                    self.produtos[link] = novo_produto
                    self.automator.run_automation(link)

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
            time.sleep(1)
