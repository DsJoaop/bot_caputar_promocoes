import requests
import logging

from src.config.setting_load import load_config
from src.model.produto import Produto

logger = logging.getLogger(__name__)


class Notificacao:
    def __init__(self):
        self.config = load_config()['telegram']
        self.base_url = f"https://api.telegram.org/bot{self.config['bot_token']}/"
        self.chat_id = self.config['chat_id']

    def enviar_mensagem(self, chat_id, mensagem, reply_markup=None):
        dados = {
            'chat_id': chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }
        if reply_markup:
            dados['reply_markup'] = reply_markup

        url = f"{self.base_url}sendMessage"
        try:
            response = requests.post(url, json=dados)
            if response.status_code == 200:
                logger.info("Mensagem enviada com sucesso!")
            else:
                logger.error("Falha ao enviar mensagem")
        except requests.RequestException as e:
            logger.exception(f"Erro ao enviar mensagem: {e}")

    def enviar_notificacao(self, produto, previous_price, current_price, discount):
        mensagem = (
            f"🎉 Desconto detectado! 🎉\n\n\n"
            f"🔗 Link: {produto.link}\n\n"
            f"💰 Preço anterior: R${previous_price:.2f}\n\n"
            f"💸 Novo preço: R${current_price:.2f}\n\n"
            f"💲 Desconto: {discount:.2f}% OFF\n\n"
            f"ℹ️ Deseja comprar este item?\n\n"
            f"Responda SIM ou NÃO para confirmar sua escolha.\n"
        )
        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
            ]
        }
        self.enviar_mensagem(self.chat_id, mensagem, reply_markup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    notify = Notificacao()
    produto = Produto("https://www.pichau.com.br/cadeira-office-zinnia-aspen-preto-zno-apn-bk", 20, "teste")
    notify.enviar_notificacao(produto,10,20,10)
