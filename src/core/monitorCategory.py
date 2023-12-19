import time
import threading


class CategoryMonitor(threading.Thread):
    def __init__(self, categoria, url, desconto_minimo, notificador, scraper):
        super().__init__()
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.scraper = scraper
        self.produtos_precos = {}

    def run(self):
        while True:
            produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)
            print(f"Monitorando produto de {self.categoria} ...")
            if produtos:
                for produto in produtos:
                    if produto.link in self.produtos_precos:
                        previous_price = self.produtos_precos[produto.link]
                        current_price = produto.price
                        discount = ((previous_price - current_price) / previous_price) * 100
                        if discount >= self.desconto_minimo:
                            mensagem = f"Desconto detectado!\nLink: {produto.link}\nPreço anterior: R${previous_price}\nNovo preço: R${current_price}\nDesconto: {discount:.2f}%"
                            self.notificador.enviar_mensagem(mensagem)

                    self.produtos_precos[produto.link] = produto.price

            else:
                print(f"Nenhum produto encontrado para a categoria: {self.categoria}")

            time.sleep(5)  # Espera 5 segundos antes de fazer o próximo scraping
