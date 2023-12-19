import pyautogui
import webbrowser
import os
import time


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
        self.timeout_seconds = 10

    def path_exists(self, image_path):
        if not os.path.exists(image_path):
            print(f"Arquivo não encontrado: {image_path}")
            return False
        return True

    def search_on_screen(self, image_path):
        if not self.path_exists(image_path):
            return

        start_time = time.time()

        while time.time() - start_time < self.timeout_seconds:
            try:
                x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                pyautogui.click(x, y)
                print("\n-----------------------------------------------------")
                print(f"{image_path} encontrado.")
                print("-----------------------------------------------------\n")

                return True
            except pyautogui.ImageNotFoundException:
                print(f"Searching for {image_path}...")

        print(f"Imagem {image_path} não encontrada após {self.timeout_seconds} segundos.")
        return False

    def run_automation(self, url):
        start_time = time.time()

        webbrowser.open(url)

        for img_path in self.img_paths:
            if img_path == self.img_paths[5]:
                time.sleep(0.3)

            if not self.search_on_screen(img_path):
                break

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tempo de execução: {execution_time} segundos")


if __name__ == "__main__":
    automator = PichauAutomator()
    automator.run_automation(
        "https://www.pichau.com.br/processador-amd-ryzen-5-7600-6-core-12-threads-3-8ghz-5-1ghz-turbo-cache-38mb-am5-100-100001015box")
