import pyautogui
import webbrowser
import os


class PichauAutomator:
    def __init__(self):
        self.img_paths = [
            'assets/pichau/1_comprar.png',
            'assets/pichau/2_finalizar_pedido.png',
            'assets/pichau/3_metodo_envio.png',
            'assets/pichau/4_continuar_pagamento.png',
            'assets/pichau/5_boleto_bancario.png',
            'assets/pichau/6_continuar_revisao.png',
            'assets/pichau/7_termos.png'
        ]

    def path_exists(self, image_path):
        if not os.path.exists(image_path):
            print(f"Arquivo não encontrado: {image_path}")
            return False
        return True

    def search_on_screen(self, image_path):
        if not self.path_exists(image_path):
            return False

        try:
            x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            return x, y
        except pyautogui.ImageNotFoundException:
            return False

    def wait_for_click(self):
        while True:
            if pyautogui.mouseDown(button='left'):
                for img_path in self.img_paths:
                    if not self.search_on_screen(img_path):
                        print(f"Imagem {img_path} não encontrada.")
                break

    def run_automation(self, url):
        webbrowser.open(url)
        self.wait_for_click()
        print("Automação concluída.")


if __name__ == "__main__":
    automator = PichauAutomator()
    automator.run_automation(
        "https://www.pichau.com.br/processador-amd-ryzen-5-7600-6-core-12-threads-3-8ghz-5-1ghz-turbo-cache-38mb-am5"
        "-100-100001015box")
