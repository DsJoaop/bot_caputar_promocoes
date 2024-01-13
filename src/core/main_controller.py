from concurrent.futures import ThreadPoolExecutor

from src.telegram.telegram_notify import Notificacao
from src.config.setting_load import load_config, carregar_produtos_desejados_pichau
from src.core.monitor_category import CategoryMonitor


class MainController:
    def __init__(self):
        self.config = load_config()
        if self.config and 'telegram' in self.config:
            self.notificador = Notificacao()
            self.desconto_minimo = 0
            self.lista_desejo = carregar_produtos_desejados_pichau()
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
        category_monitor = CategoryMonitor(categoria, url, self.desconto_minimo, self.notificador, self.lista_desejo)
        category_monitor.run()


if __name__ == "__main__":
    try:
        controller = MainController()
        controller.iniciar_monitoramento()
    except ValueError as e:
        print(f"Erro ao iniciar: {e}")
