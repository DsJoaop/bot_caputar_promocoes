import time
from src.data_acess.scraper import Scraper
from src.bot_iteration.telegram_notify import Notificacao
from src.config.setting_load import load_config
from src.core.logger import Logger


class Controller:
    def __init__(self):
        self.logger = Logger(__name__)

    def main(self):
        try:
            config_data = load_config()

            if config_data:
                telegram_config = config_data.get('telegram', {})
                bot_token = telegram_config.get('bot_token')
                chat_id = telegram_config.get('chat_id')

                if bot_token and chat_id:
                    list_urls_categorias = config_data.get('categorias', {})
                    notificacao = Notificacao(bot_token, chat_id)
                    self.monitorar_precos(list_urls_categorias, notificacao)
                else:
                    self.logger.log_error("Configurações do Telegram incompletas. Verifique o arquivo de configuração.")
            else:
                self.logger.log_error("Falha ao carregar configurações.")

        except Exception as e:
            self.logger.log_error(f"Erro inesperado: {e}")

    def monitorar_precos(self, urls_categorias, notificacao, intervalo=60):
        precos_antigos = {categoria: [] for categoria in urls_categorias}

        while True:
            try:
                for categoria, url in urls_categorias.items():
                    produtos_novos = self.obter_novos_produtos(url, categoria)

                    if produtos_novos:
                        precos_antigos[categoria] = self.comparar_precos(precos_antigos[categoria], produtos_novos,
                                                                         notificacao)

                time.sleep(intervalo)

            except Exception as e:
                self.logger.log_error(f"Erro no monitoramento de preços: {e}")

    def obter_novos_produtos(self, url, categoria):
        try:
            scraper = Scraper({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })
            return scraper.fazer_scraping_produtos(url, categoria)
        except Exception as e:
            self.logger.log_error(f"Erro ao obter novos produtos: {e}")
            return []

    def comparar_precos(self, precos_antigos, produtos_novos, notificacao, limite_percentual=0.5):
        links_antigos = {produto.link for produto in precos_antigos}

        for produto_novo in produtos_novos:
            if produto_novo.link in links_antigos:
                produto_antigo = next((p for p in precos_antigos if p.link == produto_novo.link), None)
                if produto_antigo:
                    preco_antigo = self.obter_preco_float(produto_antigo.price)
                    novo_preco = self.obter_preco_float(produto_novo.price)

                    diferenca_percentual = abs((novo_preco - preco_antigo) / preco_antigo)

                    if diferenca_percentual >= limite_percentual:
                        mensagem = f"Preço alterado de R${preco_antigo:.2f} para R${novo_preco:.2f}!\nLink: {produto_novo.link}\nCategoria: {produto_novo.category}"
                        notificacao.enviar_mensagem(mensagem)

        return produtos_novos

    def obter_preco_float(self, price):
        return float(price.replace('R$', '').replace(',', '').replace('.', ''))

    def start(self):
        self.main()


if __name__ == "__main__":
    controller = Controller()
    controller.start()
