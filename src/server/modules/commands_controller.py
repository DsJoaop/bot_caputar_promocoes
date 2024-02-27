from src.server.modules.commands_pelando import CommandPelando
from src.server.modules.commands_pichau import CommandPichau
from src.telegram.notify import Notificacao



class CommandHandler:
    def __init__(self, user_states, notify_user: Notificacao):
        self.user_states = user_states
        self.notify_user = notify_user
        self.c_pichau = CommandPichau(self.user_states,self.notify_user)
        self.c_pelando = CommandPelando(self.user_states, self.notify_user)

    def handle_start(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            welcome_message = (
                "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
                "Digite /help para ver os comandos disponíveis."
            )
            self.notify_user.enviar_mensagem(welcome_message)
        else:
            self.notify_user.enviar_mensagem("Termine o processo anterior para ver o comando!")

    def handle_stop(self, chat_id, controller):
        self.user_states[chat_id]['state'] = 'stop'
        controller.parar_monitoramento()
        bye_message = "Monitoramento pausado. Até logo!"
        self.notify_user.enviar_mensagem(bye_message)

    def handle_help(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            help_message = (
                "ℹ️ Comandos disponíveis:\n\n"
                "/start - Inicia o bot\n"
                "/stop - Pare qualquer operação do bot\n"
                "/help\n"
                "/pichau - Exibir opções de monitoramento pichau\n"
                "/pelando - Exibir opções de monitoramento pelando\n"
            )
            self.notify_user.enviar_mensagem(help_message)
        else:
            self.notify_user.enviar_mensagem("Termine o processo anterior para ver a lista de ajuda!")

    def other_command(self, user_states, chat_id, notify_user, message):
        notify_user("Houve um erro ao processar as entradas. Por favor, tente novamente mais tarde.")
        print(message)  # Apenas para depuração, pode ser removido em ambiente de produção

    def command_process(self, chat_id, notify_user, message=None):
        if self.user_states.get(chat_id, {}).get('state') in estado_espera:
            handler = estado_espera[self.user_states]
            handler(self.user_states.get(chat_id, {}).get('state'), chat_id, notify_user, message)
        else:
            notify_user.enviar_mensagem("Estado de espera indefinido")

    def handle_start_pichau(self, chat_id, pichau_monitor):
        pass

    def handle_stop_pichau(self, chat_id, pichau_monitor):
        pass

    def handle_start_pelando(self, chat_id, pichau_monitor):
        pass

    def handle_stop_pelando(self, chat_id, pichau_monitor):
        pass


estado_espera = {
    'Aguardando_links': CommandHandler.handle_waiting_links,
    'Estado_erro': CommandHandler.other_command
}
