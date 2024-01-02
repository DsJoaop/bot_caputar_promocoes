import os
import psutil
import requests
from flask import Flask, jsonify, request

from src.config.setting_load import load_config
from src.data_acess.buy_pichau import PichauAutomator
from src.server.modules.utils_server import Utils
from src.telegram.telegram_notify import Notificacao


def is_main_controller_running():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'main_controller.py' in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


class TelegramBot:
    main_controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core', 'main_controller.py'))

    def __init__(self):
        self.user_states = None
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

            # Verifica o comando recebido
            if '/start' in message_text:
                self.handle_start_command(chat_id)
            elif '/stop' in message_text:
                self.handle_stop_command(chat_id)
            elif '/help' in message_text:
                self.handle_help_command(chat_id)
            elif '/list_desejos' in message_text:
                self.handle_list_desejos_command(chat_id)
            elif '/add_desejos' in message_text:
                self.handle_add_desejos_command(chat_id)
            else:
                self.handle_process_command(chat_id)

        return jsonify({'success': True})

    def handle_start_command(self, chat_id):
        # Lógica para o comando /start
        self.user_states[chat_id]['state'] = 'start'
        welcome_message = (
            "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
            "Digite /help para ver os comandos disponíveis."
        )
        self.notify_user(welcome_message)

    def handle_stop_command(self, chat_id):
        # Lógica para o comando /stop
        self.user_states[chat_id]['state'] = 'stop'
        bye_message = "Bot finalizado. Até logo!"
        self.notify_user(bye_message)

    def handle_help_command(self, chat_id):
        # Lógica para o comando /help
        self.user_states[chat_id]['state'] = 'help'
        help_message = (
            "ℹ️ Comandos disponíveis:\n\n"
            "/start - Inicia o bot\n"
            "/list_desejos - Lista os itens na lista de desejos\n"
            "/add_desejos - Adiciona um item à lista de desejos\n"
        )
        self.notify_user(help_message)

    def handle_list_desejos_command(self, chat_id):
        self.user_states[chat_id]['state'] = 'list_desejos'

    def handle_add_desejos_command(self, chat_id):
        # Lógica para o comando /add_desejos
        self.user_states[chat_id]['state'] = 'add_desejos'
        # Implemente a lógica para adicionar um desejo à lista e notificar

    def handle_process_command(self, chat_id):
        pass


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_server()
