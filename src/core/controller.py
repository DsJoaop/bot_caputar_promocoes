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
            scraper = Scraper(self.headers)  # Passar os headers diretamente para o Scraper

            for categoria, url in categorias.items():
                produtos = scraper.fazer_scraping_produtos(url, categoria)

                if produtos:
                    # Aqui você pode processar os produtos obtidos, como enviar notificações via Telegram, etc.
                    notificador = Notificacao(self.config['telegram']['bot_token'], self.config['telegram']['chat_id'])
                    for produto in produtos:
                        mensagem = f"Novo produto encontrado!\nLink: {produto.link}\nPreço: R${produto.price}\nCategoria: {produto.category}"
                        notificador.enviar_mensagem(mensagem)
                else:
                    print(f"Nenhum produto encontrado para a categoria: {categoria}")
        else:
            print(
                "Configurações não carregadas ou categorias não encontradas. Não foi possível iniciar o monitoramento "
                "de preço.")


# Para testar a classe Controller:
if __name__ == "__main__":
    controller = Controller()
    controller.start_price_monitoring()
