import os

import requests
import logging

from dotenv import load_dotenv

from config.setting_load import load_config
from src.model.oferta import Oferta

logger = logging.getLogger(__name__)


class Notifier:
    def __init__(self):

        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._base_url = f"https://api.telegram.org/bot{self._bot_token}/"

        self._chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def delete_mensage(self, message_id):
        url = f"https://api.telegram.org/bot{self._bot_token}/deleteMessage"
        params = {
            'chat_id': self._chat_id,
            'message_id': message_id
        }
        response = requests.post(url, params=params)
        return response.json()

    def enviar_mensagem(self, mensagem, reply_markup=None):
        dados = {
            'chat_id': self._chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }
        if reply_markup:
            dados['reply_markup'] = reply_markup

        url = f"{self._base_url}sendMessage"
        try:
            response = requests.post(url, json=dados)
            if response.status_code == 200:
                logger.info("Mensagem enviada com sucesso!")
            else:
                logger.error("Falha ao enviar mensagem", response.status_code)
        except requests.RequestException as e:
            logger.exception(f"Erro ao enviar mensagem: {e}")

    def enviar_notificacao_desconto(self, product, previous_price, discount, novo_preco):
        mensagem = (
            f'<a href="{product.link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"<a href=\"{product.link}\">🔗 {product.nome}</a>\n\n"
            f"<b>🎉 Categoria: {product.category}</b>\n"
            f"<b>🔥 Desconto: {discount:.2f}% OFF</b>\n\n"
            f"💰 <b>Preço anterior:</b> R${previous_price:.2f}\n"
            f"💸 <b>Novo preço:</b> R${novo_preco:.2f}\n\n"
            f"🛒 <b>Deseja comprar?!</b>\n"
        )

        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': '/pichau_autorizar_compra'},
                 {'text': 'Não', 'callback_data': '/pichau_negar_compra'}]
            ]
        }
        self.enviar_mensagem(mensagem, reply_markup)

    def enviar_alerta_novo_produto(self, product):
        mensagem = (
            f'<a href="{product.link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"<b>🎉 Novo {product.category}</b>\n\n"
            f"<a href=\"{product.link}\">🔗 {product.nome}</a>\n\n"
            f"💰 <b>Preço:</b> R${product.price:.2f}\n\n"
            f"🛒 <b>Deseja comprar?!</b>\n"
        )

        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
            ]
        }
        self.enviar_mensagem(mensagem, reply_markup)

    def enviar_alerta_nova_promocao(self, product: Oferta):
        mensagem = str(product)
        self.enviar_mensagem(mensagem)


if __name__ == '__main__':
    noty = Notifier()
    noty.enviar_mensagem('Em manutenção')