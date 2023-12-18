from collections import defaultdict

from src.bot_iteration.telegram_notify import Notificacao
from src.config.setting_load import load_config
from src.data_acess.scraper import Scraper


class Controller:
    def __init__(self):
        self.config = load_config()  # Carregar as configurações
        self.headers = {  # Definir os headers diretamente no Controller
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def start_price_monitoring(self):
        if self.config and 'categorias' in self.config:
            categorias = self.config['categorias']
            scraper = Scraper(self.headers)

            # Usando defaultdict para agrupar produtos por categoria
            produtos_por_categoria = defaultdict(list)

            for categoria, url in categorias.items():
                produtos = scraper.fazer_scraping_produtos(url, categoria)

                if produtos:
                    produtos_por_categoria[categoria].extend(produtos)
                else:
                    print(f"Nenhum produto encontrado para a categoria: {categoria}")

            # Enviar notificações agrupadas por categoria
            notificador = Notificacao(self.config['telegram']['bot_token'], self.config['telegram']['chat_id'])
            for categoria, produtos in produtos_por_categoria.items():
                if produtos:
                    mensagem = f"Novos produtos encontrados na categoria {categoria}:\n"
                    # Limitando a 10 produtos por mensagem para evitar erros de tamanho
                    for i, produto in enumerate(produtos[:10], start=1):
                        mensagem += f"\n{i}. Link: {produto.link}\n   Preço: R${produto.price}\n"

                    notificador.enviar_mensagem(mensagem)
        else:
            print(
                "Configurações não carregadas ou categorias não encontradas. Não foi possível iniciar o monitoramento de preço.")

# Para testar a classe Controller:
if __name__ == "__main__":
    controller = Controller()
    controller.start_price_monitoring()
