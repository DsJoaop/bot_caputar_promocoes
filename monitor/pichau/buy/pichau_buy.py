import threading
import time
import webbrowser
import pyperclip
from unshortenit import UnshortenIt
from monitor.pichau.buy.image_iteration import BuyPichauImage
from monitor.pichau.data.data_pichau import PichauScraping
from src.telegram.notifier import Notifier


def open_link(link):
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(
        "C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"))
    webbrowser.get('edge').open(link)


class PichauAutomator:
    def __init__(self):
        self._price = None
        self.buy_interaction = BuyPichauImage()
        self.notifier = Notifier()
        self.scraper = PichauScraping()
        self._comprar = [False]
        self.unshortener = UnshortenIt()

    def check_and_set_buy_flag(self, link):
        price, expanded_url = self.scraper.extract_price_url(link)
        if expanded_url and ("placa-de-video" in expanded_url):
            self._comprar[0] = True
            self._price = price
            print("A váriavel de compra está ativada")
        return

    def execute_buy_automation(self, link):
        start_time = time.time()
        open_link(link)
        success = self.buy_interaction.search_on_screen(self._comprar)
        end_time = time.time()
        execution_time = end_time - start_time
        return success, execution_time

    def run_automation(self, link):
        success_buy, execution_time = self.execute_buy_automation(link)
        mensagem = ""
        if success_buy:
            try:
                produto = self.scraper.create_product(link)
                content = pyperclip.paste()
                mensagem += (
                    "<b>\n\n🎉 Compra realizada com sucesso! 🎉</b>\n\n"
                    "<b>ℹ️ Copie o código:</b> <code>{}</code>\n\n".format(content)
                )
                mensagem += produto.compra_confirmada()
                self.notifier.enviar_mensagem(mensagem)
            except:
                return
        else:
            mensagem += (
                "❌ Ooops! Algo deu errado. ❌\n\n"
                "Não foi possível gerar o código devido a uma falha na "
                "automatização de compra. Por favor, tente novamente."
            )
            success_remove = True

            if success_remove:
                mensagem += "\n\n✅ O carrinho foi limpo com sucesso ✅\n\n"
            else:
                mensagem += "\n\n❌ A automação de limpeza falhou ❌\n\n"
                self.notifier.enviar_mensagem(mensagem)
            print(mensagem)
        print(f"Tempo de execução: {execution_time} segundos.")
        print(mensagem)
        self._comprar[0] = False
        return mensagem

    def run_automation_pix(self, link):
        thread = threading.Thread(target=self.check_and_set_buy_flag, args=(link,))
        thread.start()
        return self.run_automation(link)


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/processador-amd-ryzen-5-4600g-6-core-12-threads-3-7ghz-4-2ghz-turbo-cache-11mb-am4-100-100000147box"

    # Run automation
    message = automator.run_automation_pix(url)
