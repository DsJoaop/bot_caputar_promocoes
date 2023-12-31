import time
import webbrowser
import pyperclip

from src.data_acess.iteration_image import BuyPichauImage
from src.telegram.telegram_notify import Notificacao


class PichauAutomator:
    def __init__(self):
        self.interaction = BuyPichauImage()
        self.notify = Notificacao()

    def find_image(self, img_paths, max_retry_time=5):
        retry_start_time = time.time()
        index = 0

        while time.time() - retry_start_time < max_retry_time and index < len(img_paths):
            found_initial, current_index = self.interaction.search_on_screen(img_paths[index], 0)

            if found_initial:
                index += 1
            else:
                print(f"{index} imagem não encontrada. Tentando novamente...")
                time.sleep(0.3)

        print("Não foi possível encontrar a primeira imagem após 30 segundos.")
        return False

    def run_automation(self, link, img_paths):
        start_time = time.time()
        webbrowser.open(link)
        self.interaction.img_paths = img_paths

        if self.find_image(img_paths):
            end_time = time.time()
            execution_time = end_time - start_time
            return False, execution_time

        return False, 0

    def run_remove(self, link):
        webbrowser.open(link)
        img_paths = self.interaction.get_cart_image_paths()
        index = 0

        while index < len(img_paths):
            current_image_path = img_paths[index]
            found, current_index = self.interaction.search_on_screen(current_image_path, index)

            if not found:
                if index > 0:
                    index -= 1
                else:
                    return False
            else:
                time.sleep(3)
                index += 1

        return index >= 2

    def run_automation_pix(self, link):
        img_paths_pix = self.interaction.get_pix_image_paths()
        success, execution_time = self.run_automation(link, img_paths_pix)

        if success:
            pix_content = pyperclip.paste()
            message = (
                f"<b>🎉 Compra realizada com sucesso! 🎉</b>\n\n"
                f"<b>ℹ️ Copie o código PIX:</b> <code>{pix_content}</code>\n\n"
            )

        else:
            message = (
                "❌ Ooops! Algo deu errado. ❌\n\n"
                "Não foi possível gerar o código PIX devido a uma falha na automatização de compra. \n"
                "Por favor, tente novamente."
            )

            self.notify.enviar_mensagem(message)
            success = self.run_remove(link)

            if success:
                message += "\n\n✅ O carrinho foi limpo com sucesso ✅\n\n"
                self.notify.enviar_mensagem(message)
            else:
                message += "\n\n❌ A automação de limpeza falhou ❌\n\n"
                self.notify.enviar_mensagem(message)

        print(f"Tempo de execução: {execution_time} segundos.")
        return message

    def run_automation_boleto(self, link):
        img_paths_boleto = self.interaction.get_boleto_image_paths()
        success, execution_time = self.run_automation(link, img_paths_boleto)

        if success:
            message = "🎉 Pagamento por boleto processado com sucesso! 🎉"
            print("Pagamento por boleto concluído.")
        else:
            message = "❌ Ooops! Algo deu errado com o pagamento por boleto. ❌"
            print("Falha no processamento do pagamento por boleto. Tente novamente.")
            self.notify.enviar_mensagem(message)
            self.run_remove(link)

        print(f"Tempo de execução: {execution_time} segundos.")
        return message


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/mouse-ergonomico-microsoft-2-4-ghz-wireless-pessego-222-00035"
    message = automator.run_automation_pix(url)
