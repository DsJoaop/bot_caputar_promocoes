import threading
from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters, Updater, CallbackContext

class MonitorCanais:
    def __init__(self, bot_token, personal_chat_id, channels_info):
        self.bot = Bot(token=bot_token)
        self.personal_chat_id = personal_chat_id
        self.channels_info = channels_info
        self.updater = Updater(token=bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start_monitoring(self):
        for channel_info in self.channels_info:
            channel_id = channel_info.get('id')
            self.dispatcher.add_handler(MessageHandler(Filters.chat(channel_id) & Filters.text, self.forward_message))

        self.updater.start_polling()

    def start_monitoring_threaded(self):
        monitor_thread = threading.Thread(target=self.start_monitoring)
        monitor_thread.start()

    def forward_message(self, update: Update, context: CallbackContext):
        message = update.message
        forwarded_message = f"From: {message.chat.title}\n\n{message.text}"

        self.bot.send_message(chat_id=self.personal_chat_id, text=forwarded_message)