import requests
import logging

from src.config.setting_load import load_config
from src.data_acess.scraper.extract_data_pichau import extrair_imagem_produto_pichau, criar_produto_link_pichau

logger = logging.getLogger(__name__)


class Notificacao:
    def __init__(self):
        self.config = load_config().get('telegram', {})
        self.base_url = f"https://api.telegram.org/bot{self.config.get('bot_token', '')}/"
        self.chat_id = self.config.get('chat_id', '')

    def enviar_mensagem(self, mensagem, reply_markup=None):
        dados = {'chat_id': self.chat_id, 'text': mensagem, 'parse_mode': 'HTML', 'reply_markup': reply_markup}
        url = f"{self.base_url}sendMessage"
        try:
            response = requests.post(url, json=dados)
            if response.status_code == 200:
                logger.info("Mensagem enviada com sucesso!")
            else:
                logger.error("Falha ao enviar mensagem")
        except requests.RequestException as e:
            logger.exception(f"Erro ao enviar mensagem: {e}")

    def enviar_notificacao(self, product, previous_price, discount):
        mensagem = f'<a href="{product.link_img}">&#8205;</a>' \
                   f'<a href="{product.link}">🔗 {product.nome}</a>\n\n' \
                   f'<b>🎉 Categoria: {product.category}</b>\n' \
                   f'<b>🔥 Desconto: {discount:.2f}% OFF</b>\n\n' \
                   f'💰 <b>Preço anterior:</b> R${previous_price:.2f}\n' \
                   f'💸 <b>Novo preço:</b> R${product.price:.2f}\n\n' \
                   f'🛒 <b>Deseja comprar?!</b>\n'

        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
            ]
        }

        self.enviar_mensagem(mensagem, reply_markup)

    def enviar_alerta(self, product):
        extrair_imagem_produto_pichau(product)
        mensagem = f'<a href="{product.link_img}">&#8205;</a>' \
                   f'<b>🎉 Novo {product.category}</b>\n\n' \
                   f'<a href="{product.link}">🔗 {product.nome}</a>\n\n' \
                   f'💰 <b>Preço:</b> R${product.price:.2f}\n\n' \
                   f'🛒 <b>Deseja comprar?!</b>\n'

        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
            ]
        }

        self.enviar_mensagem(mensagem, reply_markup)

    def enviar_compra_confirmada(self, product, preco_anterior, discount):
        mensagem = (
            f'<a href="{product.link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"Compra desejada confirmada! 🔥🎁\n\n"
            f"<a href=\"{product.link}\">🔗 {product.nome}</a>\n\n"
            f"<b>🎉 Categoria: {product.category}</b>\n"
            f"<b>🔥 Desconto: {discount:.2f}% OFF</b>\n\n"
            f"💰 <b>Preço anterior:</b> R${preco_anterior:.2f}\n"
            f"💸 <b>Novo preço:</b> R${product.price:.2f}\n\n"
            f"🛒 <b>Abra a pichau e veja seu boleto!</b>\n"
        )

        self.enviar_mensagem(criar_produto_link_pichau(product.link), mensagem)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    notify = Notificacao()
    produto = criar_produto_link_pichau(
        "https://www.pichau.com.br/cabo-extensor-premium-24p-pichau-ps100-rgb-240mm-branco"
        "-pch-ps100-24prgbwht")
    notify.enviar_notificacao(produto, 50, 30)
