import random
import time


class CategoryMonitor:
    def __init__(self, categoria, url, desconto_minimo, notificador, scraper):
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.scraper = scraper
        self.produtos_precos = {}

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

    def run(self):
        while True:
            produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)
            if produtos:
                for produto in produtos:
                    previous_price = self.produtos_precos.get(produto.link)
                    if previous_price is not None:
                        current_price = produto.price
                        discount = ((previous_price - current_price) / previous_price) * 100
                        if discount >= self.desconto_minimo:
                            self.enviar_notificacao(produto, previous_price, current_price, discount)

                    self.produtos_precos[produto.link] = produto.price

            else:
                print(f"Nenhum produto encontrado para a categoria: {self.categoria}")
            print(f"Analisando {self.categoria}...")
            # Aguarde um tempo aleatório entre 1 e 2 segundos antes de fazer o próximo scraping
            time.sleep(random.uniform(1, 2))

