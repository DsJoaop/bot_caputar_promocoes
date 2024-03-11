from config.setting_load import get_lista_desejos as load_wishlist
from monitor.pichau.buy.buy_iteration import PichauAutomator as PichauBuyAutomator
from monitor.pichau.core.monitor_pichau import PichauMonitorController


def start_pichau_menu():
    menu_message = (
        "Bem-vindo ao menu Pichau! Por favor, selecione uma das seguintes opções:\n\n\n"
        "1. 🤖 Monitorar - Comece a monitorar um produto.\n\n"
        "2. ❌ Stop - Pare o monitoramento de um produto.\n\n"
        "3. 🔁 Resetar - Reinicie o monitoramento de um produto.\n\n"
        "4. 🛒 Lista de Desejos - Veja sua lista de produtos monitorados.\n\n"
        "5. 🧷 Adicionar à lista - Adicione um novo produto à sua lista de desejos.\n"
    )
    reply_markup = {
        'inline_keyboard': [
            [{'text': '🤖 Monitorar', 'callback_data': '/pich_start'}, {'text': '❌ Stop', 'callback_data': '/pich_stop'}],
            [{'text': '🔁 Resetar', 'callback_data': '/pich_reset'}, {'text': '🛒 Lista Desejos', 'callback_data': '/pich_list'}],
            [{'text': '🧷 Adicionar a lista', 'callback_data': '/pich_add_list'}],
            [{'text': '🎥 Monitorar Live', 'callback_data': '/pich_start_live'}]
        ]
    }
    return menu_message, reply_markup


class PichauCommandHandler:
    def __init__(self, user_states):
        self.user_states = user_states
        self.automator = PichauBuyAutomator()
        self.monitor_controller = PichauMonitorController()

    def handle_verify_purchase(self, entities, response, product_link):
        if len(entities) > 3 and entities[1]['type'] == 'text_link':
            product_link = entities[1]['url']
        if product_link is not None and response == "sim":
            message = self.automator.run_automation_pix(product_link)
            return message
        else:
            return "Ok, compra não autorizada."

    def handle_wishlist(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            links = load_wishlist()
            if links is not None:
                a = chat_id  # Placeholder for further processing
                # products = list_products(links)
                # self.notifier.send_message(format_message(products))
            else:
                return "Erro ao carregar lista de desejos"
        else:
            return "Termine o processo anterior para ver a lista de desejos!"

    def handle_add_wishlist(self, chat_id):
        user_state = self.user_states.get(chat_id, {}).get('state')

        if user_state == 'liberado' or user_state is None:
            message = (
                "Envie os links e os preços máximos dos produtos que deseja adicionar à lista de desejos.\n\n"
                "Envie uma linha para cada produto no formato:\n\n"
                "`preço_maximo ; link_do_produto`\n\n"
                "Aguardando suas mensagens..."
            )
            return message
        else:
            return "Termine o processo anterior para ver a lista de desejos!"

    def handle_waiting_links(self, data, chat_id):
        message = data['message']['text']
        try:
            lines = message.split('\n')
            added_products = []

            for line in lines:
                parts = line.split(';')
                if len(parts) == 2:
                    price_str = parts[0].strip()
                    product_link = parts[1].strip()
                    try:
                        max_price = float(price_str)
                        # add_wishlist_product(product_link, max_price)
                        added_products.append((product_link, max_price))
                    except ValueError:
                        self.user_states[chat_id]['state'] = None
                        return "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha."
                    except Exception as e:
                        print(e)
                        self.user_states[chat_id]['state'] = None
                        return "Houve um erro ao salvar os produtos desejados. Por favor, tente novamente mais tarde."

            self.user_states[chat_id]['state'] = None

            if added_products:
                for link, price in added_products:
                    return f"O produto no link: {link} \n\nFoi adicionado à lista de desejos com um preço máximo de {price}."
            else:
                return "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha."
        except Exception as e:
            print(e)
            return "Houve um erro ao processar as entradas. Por favor, tente novamente mais tarde."

    def start_monitor(self):
        self.monitor_controller.start_monitoring()

    def stop_monitor(self):
        self.monitor_controller.stop_monitoring()

    def reset_monitor(self):
        self.monitor_controller.restart_monitoring()

    def start_live_monitor(self):
        #self.monitor_controller.start_live_monitoring()
        return

    def process_command(self, user_states, chat_id, resposta, message_id):
        if resposta == '/pich_start':
            self.start_monitor()
        elif resposta == '/pich_stop':
            self.stop_monitor()
        elif resposta == '/pich_reset':
            self.reset_monitor()
        elif resposta == '/pich_list':
            response = self.handle_wishlist(chat_id)
            # Se a resposta não for None, é porque houve algum erro.
            if response:
                print(response)  # Você pode lidar com a mensagem de erro de alguma maneira
        elif resposta == '/pich_add_list':
            response = self.handle_add_wishlist(chat_id)
            # Se a resposta não for None, é porque houve algum erro.
            if response:
                print(response)  # Você pode lidar com a mensagem de erro de alguma maneira
        elif resposta == '/pich_start_live':
            self.start_live_monitor()
        else:
            # Se o callback_data não corresponder a nenhum comando esperado
            print("Comando não reconhecido.")



