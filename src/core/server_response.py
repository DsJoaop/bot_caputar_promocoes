import subprocess
import time

import requests
from flask import Flask, jsonify, request

from src.bot_iteration.telegram_notify import Notificacao
from src.config.setting_load import load_config
from src.data_acess.pichauAutomator import PichauAutomator


class TelegramBot:
    def __init__(self):
        self.buy_automation = None
        self.base_url = None
        self.ngrok_url = None
        self.notify = None
        self.bot_token = None
        self.app = Flask(__name__)
        self.setup_bot()

    def setup_bot(self):
        config = load_config()['telegram']
        self.notify = Notificacao()
        self.bot_token = config['bot_token']
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.buy_automation = PichauAutomator()

    def get_ngrok_url(self):
        try:
            ngrok_api_url = "http://localhost:4040/api/tunnels"  # URL da API do Ngrok
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

    def configure_webhook(self, url):
        webhook_url = f"{self.base_url}setWebhook?link={url}/resposta_telegram"
        try:
            response = requests.get(webhook_url, verify=True)  # Verificar SSL
            if response.status_code == 200:
                print("Webhook configurado com sucesso!")
            else:
                print("Falha ao configurar o webhook")
        except requests.RequestException as e:
            print(f"Erro ao configurar o webhook: {e}")

    def handle_telegram_response(self):
        data = request.json  # Movendo a obtenção dos dados para dentro do método
        if data and 'callback_query' in data:
            resposta = data['callback_query']['data']
            entities = data['callback_query']['message']['entities']

            link = None
            if len(entities) > 3 and entities[3]['type'] == 'text_link':
                link = entities[3]['link']

            if link is not None and resposta == "sim":
                mensagem = self.buy_automation.run_automation_pix(link)
                self.notify_user(mensagem)
            else:
                self.notify_user("Ok, compra não autorizada!")

        return jsonify({'success': True})

    def notify_user(self, message):
        self.notify.enviar_mensagem(message)

    def run_ngrok(self):
        try:
            subprocess.Popen(["ngrok", "http", "5000"])
            time.sleep(2)  # Aguarda um pouco para o Ngrok iniciar completamente
            print("Ngrok iniciado na porta 5000.")
        except FileNotFoundError:
            print("Ngrok não encontrado. Certifique-se de que está instalado e configurado corretamente.")

    def run_server(self):
        self.run_ngrok()  # Inicia o Ngrok na porta 5000
        self.app.route('/resposta_telegram', methods=['POST'])(self.handle_telegram_response)
        self.ngrok_url = self.get_ngrok_url()
        if self.ngrok_url:
            self.configure_webhook(self.ngrok_url)
        else:
            print("Não foi possível obter o URL do ngrok.")
        self.app.run(port=5000)


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_server()
