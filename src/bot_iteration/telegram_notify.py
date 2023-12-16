import requests


class Notificacao:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"

    def enviar_mensagem(self, mensagem):
        dados = {
            'chat_id': self.chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }

        try:
            resposta = requests.post(self.base_url + 'sendMessage', data=dados)
            resposta.raise_for_status()

            resposta_json = resposta.json()
            if not resposta_json['ok']:
                raise ValueError(f"Erro ao enviar mensagem: {resposta_json.get('description')}")

        except requests.RequestException as e:
            print(f"Erro de requisição: {e}")
        except ValueError as ve:
            print(f"Erro ao enviar mensagem: {ve}")
