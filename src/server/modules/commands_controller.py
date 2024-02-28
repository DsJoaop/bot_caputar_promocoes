from src.server.modules.commands_openai import CommandOpenai
from src.server.modules.commands_pelando import CommandPelando
from src.server.modules.commands_pichau import CommandPichau, handle_start_pichau
from src.telegram.notify import Notificacao


class CommandHandler:
    def __init__(self, user_states, notify_user: Notificacao):
        self.user_states = user_states
        self.notify_user = notify_user
        self.c_pichau = CommandPichau(self.user_states)
        self.c_pelando = CommandPelando(self.user_states)
        self.botIA = CommandOpenai()

    def handle_start(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            help_message = (
                "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
                "Digite /help para ver os comandos disponíveis.\n\n"
                "ℹ️ Comandos disponíveis:\n\n"
                "stop - Pare qualquer operação do bot\n"
                "help\n"
                "pichau - Exibir opções de monitoramento pichau\n"
                "pelando - Exibir opções de monitoramento pelando\n"
            )
            reply_markup = {
                'inline_keyboard': [
                    [{'text': '/stop', 'callback_data': '/stop'}, {'text': 'help', 'callback_data': '/help'}],
                    [{'text': '/pichau', 'callback_data': '/pichau'}, {'text': 'pelando', 'callback_data': '/pelando'}]
                ]
            }
            self.notify_user.enviar_mensagem(help_message, reply_markup=reply_markup)
        else:
            self.notify_user.enviar_mensagem("Termine o processo anterior para ver a lista de ajuda!")

    def command_process(self, user_states, chat_id, message_text):
        estado = user_states[chat_id].get()
        if not estado:
            if message_text == '/stop':
                self.handle_stop_all()
                self.notify_user.enviar_mensagem("Todos os processos foram parados com sucesso!")
            elif message_text == '/pichau':
                handle_start_pichau()
            elif message_text == '/pelando':
                handle_start_pelando()
            else:
                print("Comando não reconhecido")

    def handle_bot(self, chat_id):
        pass

    def handle_stop_all(self):
        self.c_pichau.handle_stop_monitoramento()
        self.c_pelando.handle_stop_pelando()
