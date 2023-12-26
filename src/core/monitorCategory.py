import asyncio
import threading
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

    async def enviar_notificacao(self, produto, previous_price, current_price, discount):
        mensagem = (
            f"🎉 Desconto detectado! 🎉\n\n\n"
            f"🔗 Link: {produto.link}\n\n"
            f"💰 Preço anterior: R${previous_price:.2f}\n\n"
            f"💸 Novo preço: R${current_price:.2f}\n\n"
            f"💲 Desconto: {discount:.2f}% OFF\n\n"
            f"ℹ️ Deseja comprar este item?\n\n"
            f"Responda SIM ou NÃO para confirmar sua escolha.\n"
        )
        resposta = await self.notificador.enviar_mensagem_com_botao_assincrono(mensagem)
        print(resposta)
        await self.processar_resposta(resposta, produto.link)

    def comprar_produto(self, link):
        self.automator.run_automation(link)

    async def processar_resposta(self, resposta, link):
        if resposta == 'SIM':
            await asyncio.to_thread(self.comprar_produto, link)

    def run(self):
        while True:
            start_time = time.time()

            novos_produtos = self.scraper.fazer_scraping_produtos(self.url, self.categoria)

            for novo_produto in novos_produtos:
                link = novo_produto.link
                if link in self.produtos:
                    produto_anterior = self.produtos[link]
                    discount = ((produto_anterior.price - novo_produto.price) / produto_anterior.price) * 100
                    if discount >= self.desconto_minimo:
                        asyncio.run(
                            self.enviar_notificacao(novo_produto, produto_anterior.price, novo_produto.price, discount))
                        self.produtos[link] = novo_produto
                else:
                    self.produtos[link] = novo_produto

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analisando {self.categoria}... Tempo de execução: {execution_time:.4f} segundos")
            time.sleep(1)
