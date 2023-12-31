import subprocess
import time
import requests


class Utils:
    @staticmethod
    def get_ngrok_url():
        try:
            ngrok_api_url = "http://localhost:4040/api/tunnels"
            response = requests.get(ngrok_api_url)
            if response.status_code == 200:
                data = response.json()
                tunnels = data['tunnels']
                for tunnel in tunnels:
                    if tunnel['proto'] == 'https':
                        return tunnel['public_url']
            else:
                print("Falha ao obter informações do Ngrok.")
        except requests.RequestException as e:
            print(f"Erro ao acessar a API do Ngrok: {e}")
        return None

    @staticmethod
    def run_ngrok():
        try:
            subprocess.Popen(["ngrok", "http", "5000"])
            time.sleep(2)  # Aguarda um pouco para o Ngrok iniciar completamente
            print("Ngrok iniciado na porta 5000.")
        except FileNotFoundError:
            print("Ngrok não encontrado. Certifique-se de que está instalado e configurado corretamente.")
