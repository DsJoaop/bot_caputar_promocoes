from config.setting_load import get_lista_desejos
from monitor.pichau.buy.buy_pichau import PichauAutomator
from monitor.pichau.core.monitor_pichau import ControllerMonitorPichau


def handle_start_pichau():
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


class CommandPichau:
    def __init__(self, states):
        self.user_states = states
        self.automation = PichauAutomator()
        self.pichau_monitor = ControllerMonitorPichau()

    def handle_verify_buy(self, entities, resposta, link):
        if len(entities) > 3 and entities[1]['type'] == 'text_link':
            link = entities[1]['url']
        if link is not None and resposta == "sim":
            mensagem = self.automation.run_automation_pix(link)
            return mensagem
        else:
            return "Ok, compra não autorizada."

    def handle_start_monitoramento(self):
        self.pichau_monitor.iniciar_monitoramento()

    def handle_stop_monitoramento(self):
        self.pichau_monitor.parar_monitoramento()

    def handle_list_desejos(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            links = get_lista_desejos()
            if links is not None:
                a = chat_id
                # produtos = listar_produtos(links)
                # self.notify_user.enviar_mensagem(formatar_mensagem(produtos))
            else:
                return "Erro ao carregar lista de desejos"
        else:
            return "Termine o processo anterior para ver a lista de desejos!"

    def handle_add_list_desejos(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')

        if user_state == 'liberado' or user_state is None:
            mensagem = (
                "Envie os links e os preços máximos dos produtos que deseja adicionar à lista de desejos.\n\n"
                "Envie uma linha para cada produto no formato:\n\n"
                "`preço_maximo ; link_do_produto`\n\n"
                "Aguardando suas mensagens..."
            )
            return mensagem
        else:
            return "Termine o processo anterior para ver a lista de desejos!"

    def handle_waiting_links(self, data, chat_id):
        message = data['message']['text']
        try:
            linhas = message.split('\n')
            produtos_adicionados = []

            for linha in linhas:
                partes = linha.split(';')
                if len(partes) == 2:
                    preco_str = partes[0].strip()
                    link_produto = partes[1].strip()
                    try:
                        preco_maximo = float(preco_str)
                        #add_produto_desejo(link_produto, preco_maximo)
                        produtos_adicionados.append((link_produto, preco_maximo))
                    except ValueError:
                        self.user_states[chat_id]['state'] = None
                        return "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha."
                    except Exception as e:
                        print(e)
                        self.user_states[chat_id]['state'] = None
                        return "Houve um erro ao salvar os produtos desejados. Por favor, tente novamente mais tarde."

            self.user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto

            if produtos_adicionados:
                for link, preco in produtos_adicionados:
                    return f"O produto no link: {link} \n\nFoi adicionado à lista de desejos com um preço máximo de {preco}."
            else:
                return "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha."
        except Exception as e:
            print(e)
            return "Houve um erro ao processar as entradas. Por favor, tente novamente mais tarde."
