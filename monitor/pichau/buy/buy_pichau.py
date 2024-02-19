import time
import webbrowser
import pyperclip

from monitor.pichau.buy.iteration_image import BuyPichauImage
from src.telegram.notify import Notificacao


def open_link(link):
    webbrowser.open(link)
    time.sleep(2)


class PichauAutomator:
    def __init__(self):
        self.buy_interaction = BuyPichauImage()
        self.notifier = Notificacao()

    def execute_buy_automation(self, link, img_paths, max_attempts=3):
        open_link(link)
        current_index = 0
        total_image_found = 0
        start_time = time.time()

        while current_index < len(img_paths) and max_attempts > 0:
            current_image_path = img_paths[current_index]
            found, next_index = self.buy_interaction.search_on_screen(current_image_path, current_index)

            if found:
                total_image_found += 1
                time.sleep(0.2)

            current_index = next_index if found else max(current_index - 1, 0)
            max_attempts -= 1 if not found else 0

        end_time = time.time()
        execution_time = end_time - start_time

        return total_image_found == len(img_paths), execution_time

    def execute_remove_automation(self):
        img_paths = self.buy_interaction.get_cart_image_paths()
        index = 0

        while index < len(img_paths):
            current_image_path = img_paths[index]
            found, current_index = self.buy_interaction.search_on_screen(current_image_path, index)

            if not found:
                if index > 0:
                    index -= 1
                else:
                    return False
            else:
                time.sleep(3)
                index += 1

        return index >= 2

    def run_automation(self, link, img_paths):
        success_buy, execution_time = self.execute_buy_automation(link, img_paths)

        if success_buy:
            content = pyperclip.paste()
            mensagem = (
                "<b>🎉 Compra realizada com sucesso! 🎉</b>\n\n"
                "<b>ℹ️ Copie o código:</b> <code>{}</code>\n\n".format(content)
            )
        else:
            mensagem = (
                "❌ Ooops! Algo deu errado. ❌\n\n"
                "Não foi possível gerar o código devido a uma falha na "
                "automatização de compra. Por favor, tente novamente."
            )
            success_remove = self.execute_remove_automation()

            if success_remove:
                mensagem += "\n\n✅ O carrinho foi limpo com sucesso ✅\n\n"
            else:
                mensagem += "\n\n❌ A automação de limpeza falhou ❌\n\n"

        self.notifier.enviar_mensagem(mensagem)
        print(f"Tempo de execução: {execution_time} segundos.")
        return mensagem

    def run_automation_pix(self, link):
        img_paths_pix = self.buy_interaction.get_pix_image_paths()
        return self.run_automation(link, img_paths_pix)

    def run_automation_boleto(self, link):
        img_paths_boleto = self.buy_interaction.get_boleto_image_paths()
        return self.run_automation(link, img_paths_boleto)


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/interruptor-smart-zinnia-2-botoes-10a-50-60hz-branco-zns-i2b-wh01"
    message = automator.run_automation_pix(url)
