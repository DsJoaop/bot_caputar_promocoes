import random
import threading
import time

from src.data_acess.scraper.extract_data_pichau import scraping_produtos_pichau


class CategoryMonitor:
    def __init__(self, categoria, url, desconto_minimo, notificador):
        self.categoria = categoria
        self.url = url
        self.desconto_minimo = desconto_minimo
        self.notificador = notificador
        self.produtos = {}

        # Primeira execução para definir produtos iniciais
        novos_produtos = scraping_produtos_pichau(self.url)
        for produto in novos_produtos:
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
                        notification_thread = threading.Thread(
                            target=self.notificador.enviar_notificacao,
                            args=(novo_produto, produto_anterior.price, discount)
                        )
                        notification_thread.start()
                        self.produtos[link] = novo_produto
                else:
                    notification_thread = threading.Thread(
                        target=self.notificador.enviar_alerta,
                        kwargs={'product': novo_produto}  # Passando o argumento como um argumento nomeado
                    )
                    notification_thread.start()
                    self.produtos[link] = novo_produto

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
            time.sleep(random.uniform(60, 200))
