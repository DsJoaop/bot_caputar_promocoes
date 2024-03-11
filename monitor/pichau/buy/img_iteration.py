import os
import concurrent.futures
import time

import pyautogui


def _get_assets_directory():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    return os.path.abspath(os.path.join(parent_directory, '..', '..', 'assets', 'pichau'))


class BuyPichauImage:
    def __init__(self):
        self.assets_directory = _get_assets_directory()
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.img_remove = [
            '21_limpar_carrinho.png',
            '22_confirmar_limpeza.png',
            '23_nenhum_produto.png'
        ]
        self.img_path = [
            '1_comprar.png',
            '2_finalizar_pedido.png',
            '3_metodo_envio.png',
            '4_continuar_pagamento.png',
            '5_pix.png',
            '6_continuar_revisao.png',
            '7_termos.png',
            '8_finalizar_agora.png',
            '9_copiar_pix.png',
            '10_concluir.png'
        ]
        self.img_paths = self._get_image_paths(self.img_path)
        self.timeout_seconds = 0.01
        self.last_image_path = None
        self.comprar = []
        self.futures = []

    def _get_image_paths(self, image_names):
        return [os.path.join(self.assets_directory, image_name) for image_name in image_names]

    def verify_image(self, image_path, y):
        if image_path in (self.img_paths[4], self.img_paths[7]):
            time.sleep(0.8)
            return y
        elif image_path == self.img_paths[2]:
            return y + 55

    def search_on_screen(self, comprar):
        all_results = []
        self.comprar = comprar

        for _ in range(40):
            for image_path in self.img_paths:
                future = self.executor.submit(self.search_image, image_path, comprar)
                self.futures.append(future)

            for future in concurrent.futures.as_completed(self.futures):
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as exc:
                    print(f'Erro ao buscar imagem: {exc}')

            if all(all_results):
                print(f'Retornando verdadeiro')
                return True

        if self.last_image_path in self.img_path[7:10]:
            return True
        return False

    def search_image(self, image_path, comprar):
        try:
            x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.82)
            y = self.verify_image(image_path, y)

            if os.path.basename(image_path) == self.img_paths[6] and not comprar[0]:
                print("Não clicando na imagem de finalizar pagamento porque 'comprar' é False.")
                return False

            pyautogui.click(x, y)
            print(f"Encontrado {image_path}...")
            self.last_image_path = image_path
            return True
        except pyautogui.ImageNotFoundException:
            print(f"Buscando {image_path}...")
            pass

    def process_remove_images(self):
        remove_image_paths = self._get_image_paths(self.img_remove)
        for image_path in remove_image_paths:
            if self.search_image(image_path, []):
                print(f"Imagem de remoção {image_path} encontrada e processada.")
            else:
                print(f"Imagem de remoção {image_path} não encontrada.")
