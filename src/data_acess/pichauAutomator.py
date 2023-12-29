import time
import webbrowser

import pyperclip

from src.data_acess.extractPay import ImageInteraction


class PichauAutomator:
    def __init__(self):
        self.interaction = ImageInteraction()

    def find_first_image(self):
        max_retry_time = 30
        retry_start_time = time.time()

        while time.time() - retry_start_time < max_retry_time:
            found_initial, _ = self.interaction.search_on_screen(self.interaction.img_paths[0], 0)
            if found_initial:
                return True
            else:
                print("Primeira imagem não encontrada. Tentando novamente...")
                time.sleep(1)

        print("Não foi possível encontrar a primeira imagem após 30 segundos.")
        return False

    def process_images(self):
        index = 1
        while index < len(self.interaction.img_paths):
            found, current_index = self.interaction.search_on_screen(self.interaction.img_paths[index], index)
            if not found:
                if current_index > 0:
                    index = current_index - 1
                else:
                    print("Nenhuma imagem anterior para verificar. Saindo.")
                    break
            else:
                index += 1

        return index >= 8

    def run_automation(self, url):
        start_time = time.time()
        webbrowser.open(url)

        if self.find_first_image():
            success = self.process_images()
            end_time = time.time()
            execution_time = end_time - start_time

            if success:
                pix_content = pyperclip.paste()
                mensagem = (
                    f"<b>🎉 Compra realizada com sucesso! 🎉</b>\n\n"
                    f"<b>ℹ️ Copie o código PIX:</b> <code>{pix_content}</code>\n\n"
                )
                print(f"Conteúdo da área de transferência: {pix_content}")
            else:
                mensagem = (
                    "❌ Ooops! Algo deu errado. ❌\n\n"
                    "Não foi possível gerar o código PIX devido a uma falha na automatização de compra. \n"
                    "Por favor, tente novamente."
                )

            print(f"Tempo de execução: {execution_time} segundos.")
            return mensagem

        else:
            return "Falha ao iniciar a automação."


if __name__ == "__main__":
    automator = PichauAutomator()
    url = "https://www.pichau.com.br/mouse-ergonomico-microsoft-2-4-ghz-wireless-pessego-222-00035"
    mensagem = automator.run_automation(url)

    if mensagem != "Falha ao iniciar a automação.":
        print(f"Mensagem: {mensagem}")
        # Aqui você pode fazer algo com a mensagem, como enviar para outro lugar ou exibir para o usuário
    else:
        print("Falha ao realizar a compra.")
        print(f"Mensagem de falha: {mensagem}")