import time
import webbrowser

import pyperclip

from src.data_acess.extractPay import ImageInteraction


class PichauAutomator:
    def __init__(self):
        self.interaction = ImageInteraction()

    def find_first_image(self, max_retry_time=30):
        retry_start_time = time.time()

        while time.time() - retry_start_time < max_retry_time:
            found_initial, _ = self.interaction.search_on_screen(self.interaction.img_paths[0], 0)
            if found_initial:
                return True
            else:
                print("Primeira imagem não encontrada. Tentando novamente...")
                time.sleep(0.3)

        print("Não foi possível encontrar a primeira imagem após 30 segundos.")
        return False

    def process_images(self):
        index = 1
        retroces = False
        img_paths = self.interaction.img_paths  # Armazena uma referência para reduzir chamadas repetidas

        while index < len(img_paths):
            current_image_path = img_paths[index]  # Utiliza a referência armazenada
            found, current_index = self.interaction.search_on_screen(current_image_path, index)

            if not found:
                if index > 0 and not retroces:
                    retroces = True
                    index -= 1
                elif retroces:
                    retroces = False
                    index += 2
                else:
                    index += 1
            else:
                index += 1

        return index >= 8

    def run_automation(self, link, img_paths):
        start_time = time.time()
        webbrowser.open(link)

        self.interaction.img_paths = img_paths

        if self.find_first_image():
            success = self.process_images()
            end_time = time.time()
            execution_time = end_time - start_time

            if success:
                return True, execution_time
            else:
                return False, execution_time

        return False, 0

    def run_automation_pix(self, link):
        img_paths_pix = self.interaction.get_pix_image_paths()

        success, execution_time = self.run_automation(link, img_paths_pix)

        if success:
            pix_content = pyperclip.paste()
            mesage = (
                f"<b>🎉 Compra realizada com sucesso! 🎉</b>\n\n"
                f"<b>ℹ️ Copie o código PIX:</b> <code>{pix_content}</code>\n\n"
            )
            print(f"Conteúdo da área de transferência: {pix_content}")
        else:
            mesage = (
                "❌ Ooops! Algo deu errado. ❌\n\n"
                "Não foi possível gerar o código PIX devido a uma falha na automatização de compra. \n"
                "Por favor, tente novamente."
            )

        print(f"Tempo de execução: {execution_time} segundos.")

        return mesage

    def run_automation_boleto(self, link):
        img_paths_boleto = self.interaction.get_boleto_image_paths()
        success, execution_time = self.run_automation(link, img_paths_boleto)

        if success:
            mensage = "🎉 Pagamento por boleto processado com sucesso! 🎉"
            print("Pagamento por boleto concluído.")
        else:
            mensage = "❌ Ooops! Algo deu errado com o pagamento por boleto. ❌"
            print("Falha no processamento do pagamento por boleto. Tente novamente.")

        print(f"Tempo de execução: {execution_time} segundos.")
        return mensage


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/mouse-ergonomico-microsoft-2-4-ghz-wireless-pessego-222-00035"
    mensagem = automator.run_automation_boleto(url)
