from telegram import Bot
import logging


# view.py
class Notificacao:
    def enviar_mensagem_telegram(mensagem, bot_token, chat_id):
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=mensagem)
