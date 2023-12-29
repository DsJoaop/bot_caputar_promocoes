import requests
import logging

from src.config.setting_load import load_config
from src.model.produto import Produto
from src.data_acess.extractData import extrair_informacao_produto_especifico

logger = logging.getLogger(__name__)


class Notificacao:
    def __init__(self):
        self.config = load_config()['telegram']
        self.base_url = f"https://api.telegram.org/bot{self.config['bot_token']}/"
        self.chat_id = self.config['chat_id']

    def enviar_mensagem(self, mensagem, reply_markup=None):
        dados = {
            'chat_id': self.chat_id,
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

    def enviar_notificacao(self, product, previous_price, discount):
        extrair_informacao_produto_especifico(product)
        mensagem = (
            f'<a href="{product.link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"<b>🎉 Categoria: {product.category}</b>\n"
            f"<b>🔥 Desconto: {discount:.2f}% OFF</b>\n\n"
            f"<a href=\"{product.link}\">🔗 {product.nome}</a>\n\n"
            f"💰 <b>Preço anterior:</b> R${previous_price:.2f}\n"
            f"💸 <b>Novo preço:</b> R${product.price:.2f}\n\n"
            f"🛒 <b>Deseja comprar?!</b>\n"
        )

        reply_markup = {
            'inline_keyboard': [
                [{'text': 'Sim', 'callback_data': 'sim'}, {'text': 'Não', 'callback_data': 'nao'}]
            ]
        }
        self.enviar_mensagem( mensagem, reply_markup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    notify = Notificacao()
    produto = Produto("https://www.pichau.com.br/openbox-teclado-multi-basico-slim-usb-preto-tc065", 20, "Teclado")
    notify.enviar_notificacao(produto, 50, 30)
