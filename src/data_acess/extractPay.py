import pyautogui
import webbrowser
import os
import time


class PichauAutomator:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        assets_directory = os.path.abspath(os.path.join(parent_directory, '..', 'assets', 'pichau'))

        self.img_paths = [
            os.path.join(assets_directory, '1_comprar.png'),
            os.path.join(assets_directory, '2_finalizar_pedido.png'),
            os.path.join(assets_directory, '3_metodo_envio.png'),
            os.path.join(assets_directory, '4_continuar_pagamento.png'),
            os.path.join(assets_directory, '5_boleto_bancario.png'),
            os.path.join(assets_directory, '6_continuar_revisao.png'),
            os.path.join(assets_directory, '7_termos.png'),
            #os.path.join(assets_directory, '8_finalizar_agora.png')
        ]
        self.timeout_seconds = 10

    def path_exists(self, image_path):
        if not os.path.exists(image_path):
            print(f"File '{image_path}' not found.\n")
            return False
        return True

    def verify_image(self, image_path, y):
        if image_path == self.img_paths[2]:
            return y + 55
        else:
            return y

    def wait(self, image_path):
        if image_path in [self.img_paths[3], self.img_paths[5]]:
            time.sleep(0.9)

    def search_on_screen(self, image_path):
        if not self.path_exists(image_path):
            return

        start_time = time.time()
        self.wait(image_path)

        while time.time() - start_time < self.timeout_seconds:
            try:
                x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                y = self.verify_image(image_path, y)
                pyautogui.click(x, y)
                print("\n-----------------------------------------------------")
                print(f"{image_path} found.")
                print("-----------------------------------------------------\n")

                return True
            except pyautogui.ImageNotFoundException:
                print(f"Searching for {image_path}...")

        print(f"Image path '{image_path}' not found on your screen after {self.timeout_seconds} seconds.\n")
        return False

    def run_automation(self, url):
        start_time = time.time()

        webbrowser.open(url)

        for img_path in self.img_paths:
            if not self.search_on_screen(img_path):
                print(
                    f"The application was closed because it could not find the image '{img_path}' on your screen.\n")
                break

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds.")

if __name__ == "__main__":
    automator = PichauAutomator()
    automator.run_automation(
        "https://www.pichau.com.br/placa-mae-pichau-alphard-a520m-p-ddr4-socket-am4-chipset-amd-a520-pch-alpda520m-p")
