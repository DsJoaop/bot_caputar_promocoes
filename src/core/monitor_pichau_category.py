import random
import threading
import time

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

        # Primeira execução para definir produtos iniciais
        novos_produtos = scraping_produtos_pichau(self.url)
        for produto in novos_produtos:
            self.produtos[produto.link] = produto

    def verificar_desconto_produto_desejado(self, produto, preco_anterior, discount):
        if produto.link in self.produtos_desejados:
            produto_anterior = self.produtos[produto.link]
            if produto.price <= produto_anterior.max_price:
                mensagem = (
                    f'<a href="{produto.link_img}">&#8205;</a>'  # Link vazio para a imagem
                    f"Compra desejada confirmada! 🔥🎁\n\n"
                    f"<a href=\"{produto.link}\">🔗 {produto.nome}</a>\n\n"
                    f"<b>🎉 Categoria: {produto.category}</b>\n"
                    f"<b>🔥 Desconto: {discount:.2f}% OFF</b>\n\n"
                    f"💰 <b>Preço anterior:</b> R${preco_anterior:.2f}\n"
                    f"💸 <b>Novo preço:</b> R${produto.price:.2f}\n\n"
                    f"🛒 <b>Abra a pichau e veja seu boleto!</b>\n"
                )
                self.automator.run_automation_boleto(produto.link)
                notification_thread = threading.Thread(
                    target=self.notificador.enviar_mensagem,
                    args=(criar_produto_link_pichau(produto.link), mensagem)
                )
                notification_thread.start()
                return
        # Se não for um produto desejado ou não houver desconto, apenas envie a notificação
        notification_thread = threading.Thread(
            target=self.notificador.enviar_notificacao,
            args=(criar_produto_link_pichau(produto.link), preco_anterior, discount)
        )
        notification_thread.start()
        self.produtos[produto.link] = produto

    def run(self):
        while True:
            start_time = time.time()

            novos_produtos = scraping_produtos_pichau(self.url)

            for novo_produto in novos_produtos:
                link = novo_produto.link
                if link in self.produtos:
                    produto_anterior = self.produtos[link]
                    discount = ((produto_anterior.price - novo_produto.price) / produto_anterior.price) * 100
                    if discount > 0:
                        self.verificar_desconto_produto_desejado(criar_produto_link_pichau(novo_produto.link),
                                                                 produto_anterior.price, discount)
                else:
                    notification_thread = threading.Thread(
                        target=self.notificador.enviar_alerta,
                        kwargs={'product': criar_produto_link_pichau(novo_produto.link)}  # Passando o argumento como
                        # um argumento nomeado
                    )
                    notification_thread.start()
                    self.produtos[link] = novo_produto

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
            time.sleep(random.uniform(30, 100))
