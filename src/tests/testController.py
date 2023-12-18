import asyncio
import aiohttp
from bs4 import BeautifulSoup

from src.core.controller import Controller
from src.data_acess.scraper import Scraper


class TestController:
    async def simulate_price_change(self, controller_instance):
        # Simulando mudança de preço para um produto específico
        url = "URL_DO_PRODUTO"
        categoria = "Categoria_do_Produto"
        novo_preco = 70  # Novo preço do produto (simulando uma mudança)

        async with aiohttp.ClientSession() as session:
            scraper = Scraper(controller_instance.headers)
            try:
                async with session.get(url, headers=controller_instance.headers, timeout=10) as response:
                    response.raise_for_status()
                    content = await response.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    card = soup.find(attrs={"data-cy": "list-product"})
                    produto = scraper.extrair_informacoes_produto(card, categoria)

                    # Simulação de mudança de preço - definindo um novo preço para o produto
                    controller_instance.previous_prices[produto.link] = novo_preco

            except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                print(f"Falha ao obter a página {url}: {e}")

    async def test_controller(self):
        controller = Controller()
        print("Simulando preço anterior...")
        await self.simulate_price_change(controller)
        print("Iniciando monitoramento de preços...")
        await controller.start_price_monitoring()
        print("Monitoramento concluído.")

# Para testar a classe de teste:
if __name__ == "__main__":
    test = TestController()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.test_controller())
