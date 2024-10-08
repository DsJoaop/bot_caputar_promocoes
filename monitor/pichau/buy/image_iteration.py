import pyautogui
import os
import time
import concurrent.futures


def path_exists(image_path):
    if not os.path.exists(image_path):
        print(f"Arquivo '{image_path}' não encontrado.\n")
        return False
    return True


class BuyPichauImage:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        assets_directory = os.path.abspath(os.path.join(parent_directory, '..', '..', 'assets', 'pichau'))

        self.img_paths = [
            '1_comprar.png',
            '2_finalizar_pedido.png',
            '3_metodo_envio.png',
            '4_continuar_pagamento.png',
            '5_pix.png',
            '6_continuar_revisao.png',
            '7_termos.png',
            '8_finalizar_agora.png',
        ]
        self.assets_directory = assets_directory
        self.timeout_seconds = 0.1
        self.last_image_path = None

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

    def get_cart_image_paths(self):
        img_paths_cart = [
            '20_carrinho.png',
            '21_limpar_carrinho.png',
            '22_confirmar_limpeza.png',
            '23_nenhum_produto.png'
        ]
        return self.get_image_paths(img_paths_cart)

    def add_extended_images(self, image_paths):
        self.img_paths += image_paths

    def verify_image(self, image_path, y):
        if os.path.basename(image_path) == self.img_paths[2]:
            return y + 55
        else:
            return y

    def search_on_screen(self, image_paths, comprar):
        all_results = []

        for _ in range(30):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for image_path in image_paths:
                    future = executor.submit(self.search_image, image_path, comprar)
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        all_results.append(result)
                    except Exception as exc:
                        print(f'Erro ao buscar imagem: {exc}')

        # Verifica se todos os resultados são True
        if all(all_results):
            print(f'Retornando verdadeiro')
            return True

        # Verifica se a última imagem é uma das três últimas
        if self.last_image_path in image_paths[7:10]:
            return True

        return False

    def search_image(self, image_path, comprar):
        start_time = time.time()
        while time.time() - start_time < self.timeout_seconds:
            try:
                x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.82)
                y = self.verify_image(image_path, y)

                if os.path.basename(image_path) == self.img_paths[6] and not comprar[0]:
                    print("Não clicando na imagem de finalizar pagamento porque 'comprar' é False.")
                    return False
                elif os.path.basename(image_path) == self.img_paths[6] or os.path.basename(image_path) == \
                        self.img_paths[4]:
                    pyautogui.click(x, y)
                    time.sleep(0.9)
                    print(f"Encontrado {image_path}...")
                    self.last_image_path = image_path
                    return True

                pyautogui.click(x, y)
                print(f"Encontrado {image_path}...")
                self.last_image_path = image_path
                return True
            except pyautogui.ImageNotFoundException:
                pass
        return False
