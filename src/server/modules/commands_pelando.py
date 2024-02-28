from monitor.pelando.core.monitor_pelando import ControllerMonitorPelando


def handle_start_pelando():
    menu_message = (
        "Bem-vindo ao menu Pichau! Selecione uma opção:\n"
        "1. Ver lista de desejos\n"
        "2. Adicionar à lista de desejos\n"
        "3. Voltar ao menu principal"
    )
    reply_markup = {
        'inline_keyboard': [
            [{'text': 'Iniciar Monitoramento', 'callback_data': '/start_monitoramento'},
             {'text': 'Parar Monitoramento', 'callback_data': '/stop_monitoramento'}],
            [{'text': 'Ajuda', 'callback_data': '/help_pichau'}, {'text': '/pichau', 'callback_data': '/pichau'}],
            [{'text': '/pelando', 'callback_data': '/pelando'}]
        ]
    }
    return menu_message, reply_markup


class CommandPelando:
    def __init__(self, states):
        self.user_states = states
        self.pelando_monitor = ControllerMonitorPelando()

    def handle_start_pelando(self, chat_id):
        pass

    def handle_stop_pelando(self):
        pass
