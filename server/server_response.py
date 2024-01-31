import requests
from flask import Flask, jsonify, request

from config.setting_load import load_config
from server.modules.commands import *
from server.modules.ngrok_config import run_ngrok, get_ngrok_url
from src.core_monitor_chats.controller_chat import MonitorCanais
from src.share.buy_pichau.buy_pichau import PichauAutomator
from src.share.telegram.telegram_notify import Notificacao


class TelegramBot:

    def __init__(self):
        config = load_config()['telegram']
        self.user_states = {}
        self.bot_token = config['bot_token']
        self.buy_automation = PichauAutomator()
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.ngrok_url = None
        self.notify = Notificacao()
        self.commands = {
            '/start': command_start,
            '/stop': command_stop,
            '/help': command_help,
            '/list_desejos': command_list_desejos,
            '/add_desejos': command_add_list_desejos
        }
        self.app = Flask(__name__)

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

    def process_command_telegram(self):
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
                command_process(self.user_states, chat_id, self.notify_user, data)
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

    def run_server(self):
        run_ngrok()

        monitor = MonitorCanais(
            bot_token=self.bot_token,
            personal_chat_id=self.ngrok_url,
            channels_info=load_config()['telegram']["canais_promo_id"]
        )
        monitor.start_monitoring_threaded()

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
