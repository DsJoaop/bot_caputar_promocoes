import threading
import time
import webbrowser
import pyperclip
from unshortenit import UnshortenIt

from monitor.pichau.buy.buy_pichau import PichauAutomatorOld
from monitor.pichau.buy.old_iteration import BuyPichauImage
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
        self.auto = PichauAutomatorOld()

    def check_and_set_buy_flag(self, link):
        price, expanded_url = self.scraper.extract_price_url(link)
        if expanded_url and ("placa-de-video" in expanded_url):
            self._comprar[0] = True
            self._price = price
            print("A váriavel de comrpa está ativada")

    def execute_buy_automation(self, link, img_paths):
        start_time = time.time()
        open_link(link)
        success = self.buy_interaction.search_on_screen(img_paths, self._comprar)
        end_time = time.time()
        execution_time = end_time - start_time
        return success, execution_time

    def run_automation(self, link, img_paths):
        success_buy, execution_time = self.execute_buy_automation(link, img_paths)
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
            success_remove = self.auto.execute_remove_automation()

            if success_remove:
                mensagem += "\n\n✅ O carrinho foi limpo com sucesso ✅\n\n"
            else:
                mensagem += "\n\n❌ A automação de limpeza falhou ❌\n\n"
                self.notifier.enviar_mensagem(mensagem)
            print(mensagem)
        print(f"Tempo de execução: {execution_time} segundos.")
        print(mensagem)
        self._comprar = False
        return mensagem

    def run_automation_pix(self, link):
        img_paths_pix = self.buy_interaction.get_pix_image_paths()
        thread = threading.Thread(target=self.check_and_set_buy_flag, args=(link,))
        thread.start()
        return self.run_automation(link, img_paths_pix)

    def run_automation_boleto(self, link):
        img_paths_boleto = self.buy_interaction.get_boleto_image_paths()
        return self.run_automation(link, img_paths_boleto)


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/adaptador-de-tomada-md9-2p-t-branco-nbr14136-branco"

    # Run automation
    message = automator.run_automation_pix(url)
