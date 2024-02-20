from concurrent.futures import ProcessPoolExecutor

from monitor.pelando.core.analyze_pelando import AnalyzePelando
from src.controller.base_main import BaseMain
from src.telegram.notify import Notificacao


class ControllerMonitorPelando(BaseMain):
    def __init__(self):
        super().__init__()
        if self._config and 'telegram' in self._config:
            self.notificador = Notificacao()
            self.desconto_minimo = 0
            self.lista_desejo = []
            self.running = False
        else:
            raise ValueError("Configurações do Telegram não encontradas no arquivo de configuração.")

    def dividir_categorias(self):
        if self._config and 'promocoes' in self._config:
            self.running = True
            self.lista_desejo = []

            with ProcessPoolExecutor() as executor:
                for categoria, url in self._config['promocoes'].items():
                    executor.submit(self.monitorar_categoria, categoria, url)
        else:
            print(
                "Configurações não carregadas ou categorias não encontradas."
                " Não foi possível iniciar o monitoramento de preço.")

    def iniciar_monitoramento(self):
        if not self.running:
            self.dividir_categorias()

    def parar_monitoramento(self):
        self.running = False

    def reiniciar_monitoramento(self):
        self.parar_monitoramento()
        self.iniciar_monitoramento()

    def monitorar_categoria(self, categoria, url):
        while self.running:
            category_monitor = AnalyzePelando(categoria, url, self.get_controller_links(), [], self.get_notify())
            category_monitor.run()


def main():
    monitoramento = ControllerMonitorPelando()
    monitoramento.iniciar_monitoramento()


if __name__ == "__main__":
    main()

