import os
import requests
from flask import Flask, jsonify, request

from src.config.setting_load import load_config
from src.data_acess.buy_pichau import PichauAutomator
from src.server.modules.utils_server import Utils
from src.telegram.telegram_notify import Notificacao


class TelegramBot:
    main_controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core', 'main_controller.py'))

    def __init__(self):
        self.user_states = None
        self.buy_automation = None
        self.base_url = None
        self.ngrok_url = None
        self.notify = None
        self.bot_token = None
        self.commands = None
        self.app = Flask(__name__)
        self.setup_bot()

    def setup_bot(self):
        config = load_config()['telegram']
        self.notify = Notificacao()
        self.bot_token = config['bot_token']
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.buy_automation = PichauAutomator()
        self.commands = {
            '/start': Utils.handle_start_command,
            '/stop': Utils.handle_stop_command,
            '/help': Utils.handle_help_command,
            '/list_desejos': Utils.handle_list_desejos_command,
            '/add_desejos': Utils.handle_add_desejos_command
        }
        self.user_states = {}

    def notify_user(self, message):
        self.notify.enviar_mensagem(message)

    def configure_webhook(self, url):
        webhook_url = f"{self.base_url}setWebhook?url={url}/resposta_telegram"
        try:
            response = requests.get(webhook_url, verify=True)  # Verificar SSL
            if response.status_code == 200:
                print("Webhook configurado com sucesso!")
            else:
                print("Falha ao configurar o webhook")
        except requests.RequestException as e:
            print(f"Erro ao configurar o webhook: {e}")

    def run_server(self):
        Utils.run_ngrok()  # Inicia o Ngrok na porta 5000
        self.app.route('/resposta_telegram', methods=['POST'])(self.handle_telegram_response)
        self.ngrok_url = Utils.get_ngrok_url()
        if self.ngrok_url:
            self.configure_webhook(self.ngrok_url)
        else:
            print("Não foi possível obter o URL do ngrok.")
        self.app.run(port=5000)

    def handle_telegram_response(self):
        data = request.json

        if data and 'message' in data and 'text' in data['message']:
            message_text = data['message']['text']
            chat_id = data['message']['chat']['id']

            if chat_id not in self.user_states:
                self.user_states[chat_id] = {}

            for command, handler in self.commands.items():
                if command in message_text:
                    handler(self.user_states, chat_id, self.notify_user, data)
                    break
            else:
                Utils.handle_process_command(self.user_states, chat_id, self.notify_user, data)
        else:
            resposta = data['callback_query']['data']
            entities = data['callback_query']['message']['entities']

            link = None
            if len(entities) > 3 and entities[1]['type'] == 'text_link':
                link = entities[1]['url']

            if link is not None and resposta == "sim":
                mensagem = self.buy_automation.run_automation_pix(link)
                self.notify_user(mensagem)
            else:
                self.notify_user("Ok, compra não autorizada!")
        return jsonify({'success': True})


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_server()
