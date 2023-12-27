from concurrent.futures import ThreadPoolExecutor
from src.bot_iteration.telegram_notify import Notificacao
from src.config.setting_load import load_config
from src.core.monitorCategory import CategoryMonitor
from src.data_acess.extractData import Scraper


class MainController:
    def __init__(self):
        self.config = load_config()
        if self.config and 'telegram' in self.config:
            self.notificador = Notificacao()
            self.scraper = Scraper(
                {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.3'
                }
            )
            self.desconto_minimo = 0
        else:
            raise ValueError("Configurações do Telegram não encontradas no arquivo de configuração.")

    def iniciar_monitoramento(self):
        if self.config and 'categorias' in self.config:
            with ThreadPoolExecutor(max_workers=10) as executor:
                for categoria, url in self.config['categorias'].items():
                    executor.submit(self.monitorar_categoria, categoria, url)
        else:
            print(
                "Configurações não carregadas ou categorias não encontradas."
                " Não foi possível iniciar o monitoramento de preço.")

    def monitorar_categoria(self, categoria, url):
        category_monitor = CategoryMonitor(categoria, url, self.desconto_minimo, self.notificador, self.scraper)
        category_monitor.run()


if __name__ == "__main__":
    try:
        controller = MainController()
        controller.iniciar_monitoramento()
    except ValueError as e:
        print(f"Erro ao iniciar: {e}")
