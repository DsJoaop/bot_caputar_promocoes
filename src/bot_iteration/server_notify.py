from flask import Flask, jsonify, request
import requests

from src.bot_iteration.telegram_notify import Notificacao
from src.config.setting_load import load_config
from src.data_acess.extractPay import PichauAutomator


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
        self.ngrok_url = config['ngrok_url']
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.buy_automation = PichauAutomator()

    def configure_webhook(self, url):
        webhook_url = f"{self.base_url}setWebhook?url={url}"
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
            chat_id = data['callback_query']['message']['chat']['id']
            mensagem = data['callback_query']['message']['text']

            indice_inicio_link = mensagem.find('🔗 Link: ') + len('🔗 Link: ')
            indice_final_link = mensagem.find('\n', indice_inicio_link)
            link = mensagem[indice_inicio_link:indice_final_link]

            if resposta == "sim":
                self.buy_automation.run_automation(link)
                self.notify_user(chat_id, resposta)
            else:
                self.notify_user(chat_id, "Ok, compra não autorizada!")

        return jsonify({'success': True})

    def notify_user(self, chat_id, message):
        self.notify.enviar_mensagem(chat_id, message)

    def run_server(self):
        self.app.route('/resposta_telegram', methods=['POST'])(self.handle_telegram_response)
        self.configure_webhook(self.ngrok_url)
        self.app.run(port=5000)


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_server()
