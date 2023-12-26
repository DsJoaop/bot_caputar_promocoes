import requests
from flask import Flask, request, jsonify
import logging

from src.config.setting_load import load_config

app = Flask(__name__)
logger = logging.getLogger(__name__)


class Notificacao:
    def __init__(self, conf):
        self.config = conf
        self.base_url = f"https://api.telegram.org/bot{self.config['bot_token']}/"
        self.configurar_webhook()
        self.chat_id = self.config['chat_id']

    def configurar_webhook(self):
        webhook_url = self.config['ngrok_url']
        api_url = f"https://api.telegram.org/bot{self.config['bot_token']}/setWebhook?url={webhook_url}"

        try:
            response = requests.get(api_url, verify=True)  # Verificar SSL
            if response.status_code == 200:
                print("Webhook configurado com sucesso!")
            else:
                print("Falha ao configurar o webhook")
        except requests.RequestException as e:
            print(f"Erro ao configurar o webhook: {e}")

    def enviar_mensagem_com_botao(self, mensagem):  # Apenas um parâmetro 'mensagem' é esperado
        dados = {
            'chat_id': self.chat_id,  # Usa 'self.chat_id', mas 'chat_id' não é passado como argumento
            'text': mensagem,
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
                ]
            },
            'parse_mode': 'HTML'
        }

        try:
            resposta = requests.post(self.base_url + 'sendMessage', json=dados, verify=True)  # Verificar SSL
            resposta.raise_for_status()
            return resposta.json()

        except requests.RequestException as e:
            print(f"Erro de requisição: {e}")
            return None

    def enviar_mensagem(self, chat_id, mensagem):
        dados = {
            'chat_id': chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }

        try:
            resposta = requests.post(self.base_url + 'sendMessage', json=dados, verify=True)
            resposta.raise_for_status()
            return resposta.json()

        except requests.RequestException as e:
            print(f"Erro de requisição: {e}")
            return None


configuracao = load_config()
notify = Notificacao(configuracao['telegram'])


@app.route('/resposta_telegram', methods=['POST'])
def resposta_telegram():
    data = request.json

    if 'callback_query' in data:
        resposta = data['callback_query']['data']
        chat_id = data['callback_query']['message']['chat']['id']

        notify.enviar_mensagem(chat_id, f"Você escolheu '{resposta.capitalize()}'")

    return jsonify({'success': True})


if __name__ == "__main__":
    config = load_config()
    notificacao = Notificacao(config['telegram'])
    notificacao.enviar_mensagem_com_botao("Escolha 'Sim' ou 'Não'")
    app.run(port=5000)