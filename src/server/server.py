import requests
from flask import Flask, jsonify, request
from src.controller.base_main import BaseMain
from src.controller.controller_scraps import ControllerScraps
from src.server.modules.commands_controller import *
from src.server.modules.ngrok import run_ngrok, get_ngrok_url


class TelegramBot(BaseMain):

    def __init__(self):
        super().__init__()
        self.user_states = {}
        self.base_url = f"https://api.telegram.org/bot{self.get_bot_token()}/"
        self.ngrok_url = None
        self.controller_links = ControllerScraps()
        self.command_handler = CommandHandler(self.user_states, self.get_notify())
        self.app = Flask(__name__)

    def notify_user(self, message):
        self._notificador.enviar_mensagem(message)

    def configure_webhook(self, url):
        webhook_url = f"{self.base_url}setWebhook?url={url}/resposta_telegram"
        try:
            response = requests.get(webhook_url, verify=True)
            if response.status_code == 200:
                print("Webhook configurado com sucesso!")
            else:
                print("Falha ao configurar o webhook")
        except requests.RequestException as e:
            print(f"Erro ao configurar o webhook: {e}")

    def process_command_telegram(self):
        data = request.json

        if data and 'message' in data and 'text' in data['message']:
            # Process regular messages
            message_text = data['message']['text']
            chat_id = data['message']['chat']['id']

            if chat_id not in self.user_states:
                self.user_states[chat_id] = {}

            if '/start' in message_text:
                self.command_handler.handle_start(chat_id)
            else:
                self.command_handler.handle_bot(chat_id)

        elif data and 'callback_query' in data and 'data' in data['callback_query']:
            chat_id = data['callback_query']['message']['chat']['id']
            resposta = data['callback_query']['data']
            message_id = data['callback_query']['message']['message_id']
            self.command_handler.command_process(self.user_states, chat_id, resposta,message_id)

        return jsonify({'success': True})

    def run_server(self):
        run_ngrok()
        self.app.route('/resposta_telegram', methods=['POST'])(self.process_command_telegram)
        self.ngrok_url = get_ngrok_url()
        if self.ngrok_url:
            self.configure_webhook(self.ngrok_url)
        else:
            print("Não foi possível obter o URL do ngrok.")

        self.app.run(port=5000)


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_server()
