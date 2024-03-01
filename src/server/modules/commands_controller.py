from src.server.modules.commands_openai import CommandOpenai
from src.server.modules.commands_pelando import CommandPelando
from src.server.modules.commands_pichau import PichauCommandHandler, start_pichau_menu
from src.telegram.notifier import Notifier


class CommandHandler:
    def __init__(self, user_states, notify_user: Notifier):
        self.user_states = user_states
        self.notifier = notify_user
        self.c_pichau = PichauCommandHandler(self.user_states)
        self.c_pelando = CommandPelando(self.user_states)
        self.botIA = CommandOpenai()

    def handle_start(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            help_message = (
                "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
                "ℹ️ Comandos disponíveis:\n\n"
                "stop - Pare qualquer operação do bot\n"
                "help\n"
                "pichau - Exibir opções de monitoramento pichau\n"
                "pelando - Exibir opções de monitoramento pelando\n"
            )
            reply_markup = {
                'inline_keyboard': [
                    [{'text': '❌ Stop', 'callback_data': '/main_stop'}, {'text': '😭 Help', 'callback_data': '/main_help'}],
                    [{'text': '🤖 Pichau', 'callback_data': '/main_pichau'}, {'text': '🤖 Pelando', 'callback_data': '/main_pelando'}]
                ]
            }
            self.notifier.enviar_mensagem(help_message, reply_markup=reply_markup)
        else:
            self.notifier.enviar_mensagem("Termine o processo anterior para ver a lista de ajuda!")

    def command_process(self, user_states, chat_id, message_text, mensage_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if not user_state:
            if message_text == '/main_stop':
                self.handle_stop_all()
                self.notifier.delete_mensage(mensage_id)
                self.notifier.enviar_mensagem("Todos os processos foram parados com sucesso!")
            elif message_text == '/main_pichau':
                mensagem, markup = start_pichau_menu()
                self.notifier.delete_mensage(mensage_id)
                self.notifier.enviar_mensagem(mensagem, markup)
            elif message_text == '/main_stop':
                mensagem = self.handle_stop_all()
                self.notifier.delete_mensage(mensage_id)
                self.notifier.enviar_mensagem(mensagem)
            elif message_text == '/main_pelando':
                 print("pelando")
            else:
                print("Comando não reconhecido")

    def handle_bot(self, message_id, resposta):
        mensagem = self.botIA.generate_response(resposta)
        self.notifier.delete_mensage(message_id)
        self.notifier.enviar_mensagem(mensagem)

    def handle_stop_all(self):
        self.c_pichau.stop_monitor()
        self.c_pelando.handle_stop_pelando()
        return 'Todos os processos foram parados'
