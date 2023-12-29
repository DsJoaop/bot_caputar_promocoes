import pyautogui
import os
import time


class ImageInteraction:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        assets_directory = os.path.abspath(os.path.join(parent_directory, '..', 'assets', 'pichau'))

        self.img_paths = [
            '1_comprar.png',
            '2_finalizar_pedido.png',
            '3_metodo_envio.png',
            '4_continuar_pagamento.png',
            '5_pix.png',
            '6_continuar_revisao.png',
            '7_termos.png',
            # '8_finalizar_agora.png',
        ]
        self.assets_directory = assets_directory
        self.timeout_seconds = 2

    def get_image_paths(self, image_names):
        return [os.path.join(self.assets_directory, image_name) for image_name in image_names]

    def get_pix_image_paths(self):
        img_paths_pix = self.img_paths[:]
        img_paths_pix[4] = '5_pix.png'
        img_paths_pix = img_paths_pix + [
            '9_copiar_pix.png',
            '10_concluir.png'
        ]
        return self.get_image_paths(img_paths_pix)

    def get_boleto_image_paths(self):
        img_paths_boleto = self.img_paths[:]
        img_paths_boleto[4] = '5_boleto_bancario.png'
        return self.get_image_paths(img_paths_boleto)

    def add_extended_images(self, image_paths):
        self.img_paths += image_paths


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

    def search_on_screen(self, image_path, index):
        if not self.path_exists(image_path):
            return False, index

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

                return True, index
            except pyautogui.ImageNotFoundException:
                print(f"Searching for {image_path}...")

        print(f"Image path '{image_path}' not found on your screen after {self.timeout_seconds} seconds.\n")
        return False, index
