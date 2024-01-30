from concurrent.futures import ThreadPoolExecutor
import threading

from src.core_products.analyze_category import AnalyzeCategory
from src.share.telegram.telegram_notify import Notificacao
from config.setting_load import load_config, carregar_produtos_desejados_pichau


class ControllerMonitor:
    def __init__(self):
        self.config = load_config()
        if self.config and 'telegram' in self.config:
            self.notificador = Notificacao()
            self.desconto_minimo = 0
            self.lista_desejo = carregar_produtos_desejados_pichau()
            self.running = False  # Adiciona um sinalizador para controlar o estado de execução
            self.monitoramento_thread = None  # Armazena a referência à thread de monitoramento
        else:
            raise ValueError("Configurações do Telegram não encontradas no arquivo de configuração.")

    def dividir_categorias(self):
        if self.config and 'categorias' in self.config:
            self.running = True  # Define o sinalizador como True para iniciar o monitoramento
            self.lista_desejo = carregar_produtos_desejados_pichau()
            with ThreadPoolExecutor(max_workers=10) as executor:
                for categoria, url in self.config['categorias'].items():
                    executor.submit(self.monitorar_categoria, categoria, url)
        else:
            print(
                "Configurações não carregadas ou categorias não encontradas."
                " Não foi possível iniciar o monitoramento de preço.")

    def iniciar_monitoramento(self):
        if not self.running:
            self.monitoramento_thread = threading.Thread(target=self.dividir_categorias)
            self.monitoramento_thread.start()

    def parar_monitoramento(self):
        self.running = False

    def reiniciar_monitoramento(self):
        self.parar_monitoramento()
        self.iniciar_monitoramento()

    def monitorar_categoria(self, categoria, url):
        while self.running:
            category_monitor = AnalyzeCategory(categoria, url, self.desconto_minimo, self.notificador,
                                               self.lista_desejo)
            category_monitor.run()

