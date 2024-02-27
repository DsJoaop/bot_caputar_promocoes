import requests
from flask import Flask, jsonify, request

from monitor.pelando.core.monitor_pelando import ControllerMonitorPelando
from monitor.pichau.core.monitor_pichau import ControllerMonitorPichau
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
        self.pichau_monitor = ControllerMonitorPichau()
        self.pelando_monitor = ControllerMonitorPelando()
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

            # Handle different commands based on message text
            if '/start' in message_text:
                self.command_handler.handle_start(chat_id)
            elif '/stop_pichau' in message_text:
                self.command_handler.handle_stop_pichau(chat_id, self.pichau_monitor)
            elif '/monitorar_pichau' in message_text:
                self.command_handler.handle_start_pichau(chat_id, self.pichau_monitor)
            elif '/parar_monitoramento_pichau' in message_text:
                self.command_handler.handle_stop(chat_id, self.pichau_monitor)
            elif '/monitorar_pelando' in message_text:
                self.command_handler.handle_start_pelando(chat_id, self.pichau_monitor)
            elif '/parar_monitoramento_pelando' in message_text:
                self.command_handler.handle_stop_pelando(chat_id, self.pichau_monitor)
            elif '/help' in message_text:
                self.command_handler.handle_help(chat_id)
            elif '/list_desejos' in message_text:
                self.command_handler.handle_list_desejos(chat_id)
            elif '/add_desejos' in message_text:
                self.command_handler.handle_add_list_desejos(chat_id)
            else:
                self.command_handler.command_process(self.user_states, chat_id, self.get_notify())

        elif data and 'callback_query' in data and 'data' in data['callback_query']:
            # Process callback queries
            resposta = data['callback_query']['data']
            entities = data['callback_query']['message']['entities']

            link = None
            if len(entities) > 3 and entities[1]['type'] == 'text_link':
                link = entities[1]['url']
            if link is not None and resposta == "sim":
                mensagem = self.get_buy_pichau().run_automation_pix(link)
                self.notify_user(mensagem)
            else:
                self.notify_user("Ok, compra não autorizada.")

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
