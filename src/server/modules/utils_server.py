import subprocess
import time
import requests

from src.config.setting_load import get_lista_desejos, add_produto_desejo
from src.data_acess.scraper.extract_data_pichau import listar_produtos, formatar_mensagem


class Utils:
    @staticmethod
    def get_ngrok_url():
        try:
            ngrok_api_url = "http://localhost:4040/api/tunnels"
            response = requests.get(ngrok_api_url)
            if response.status_code == 200:
                data = response.json()
                tunnels = data['tunnels']
                for tunnel in tunnels:
                    if tunnel['proto'] == 'https':
                        return tunnel['public_url']
            else:
                print("Falha ao obter informações do Ngrok.")
        except requests.RequestException as e:
            print(f"Erro ao acessar a API do Ngrok: {e}")
        return None

    @staticmethod
    def run_ngrok():
        try:
            subprocess.Popen(["ngrok", "http", "5000"])
            time.sleep(2)
            print("Ngrok iniciado na porta 5000.")
        except FileNotFoundError:
            print("Ngrok não encontrado. Certifique-se de que está instalado e configurado corretamente.")

    @staticmethod
    def handle_start_command(user_states, chat_id, notify_user, message=None):
        user_state = user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            welcome_message = (
                "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
                "Digite /help para ver os comandos disponíveis."
            )
            notify_user(welcome_message)
        else:
            notify_user("Termine o processo anterior para ver o comando!")

    @staticmethod
    def handle_stop_command(user_states, chat_id, notify_user, message=None):
        user_states[chat_id]['state'] = 'stop'
        bye_message = "Bot finalizado. Até logo!"
        notify_user(bye_message)

    @staticmethod
    def handle_help_command(user_states, chat_id, notify_user, message=None):
        user_state = user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            help_message = (
                "ℹ️ Comandos disponíveis:\n\n"
                "/start - Inicia o bot\n"
                "/list_desejos - Lista os itens na lista de desejos\n"
                "/add_desejos - Adiciona um item à lista de desejos\n"
            )
            notify_user(help_message)
        else:
            notify_user("Termine o processo anterior para ver a lista de ajuda!")

    @staticmethod
    def handle_list_desejos_command(user_states, chat_id, notify_user, message=None):
        user_state = user_states.get(chat_id, {}).get('state')
        if user_state == 'liberado' or user_state is None:
            links = get_lista_desejos()
            if links is not None:
                produtos = listar_produtos(links)
                notify_user(formatar_mensagem(produtos))
            else:
                notify_user("Erro ao carregar lista de desejos")
        else:
            notify_user("Termine o processo anterior para ver a lista de desejos!")

    @staticmethod
    def handle_add_desejos_command(user_states, chat_id, notify_user, message):
        user_state = user_states.get(chat_id, {}).get('state')

        if user_state == 'liberado' or user_state is None:
            mensagem = (
                "Envie os links e os preços máximos dos produtos que deseja adicionar à lista de desejos.\n\n"
                "Envie uma linha para cada produto no formato:\n\n"
                "`preço_maximo ; link_do_produto`\n\n"
                "Aguardando suas mensagens..."
            )
            notify_user(mensagem)
            user_states[chat_id]['state'] = 'Aguardando_links'
        else:
            notify_user("Termine o processo anterior para ver a lista de desejos!")

    @staticmethod
    def handle_waiting_links(user_states, chat_id, notify_user, data):
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
                        add_produto_desejo(link_produto, preco_maximo)
                        produtos_adicionados.append((link_produto, preco_maximo))
                    except ValueError:
                        notify_user(
                            "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha.")
                        user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto
                        return
                    except Exception as e:
                        print(e)
                        notify_user(
                            "Houve um erro ao salvar os produtos desejados. Por favor, tente novamente mais tarde.")
                        user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto
                        return

            user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto

            if produtos_adicionados:
                for link, preco in produtos_adicionados:
                    notify_user(
                        f"O produto no link: {link} \n\nFoi adicionado à lista de desejos com um preço máximo de {preco}.")
            else:
                notify_user("Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha.")
        except Exception as e:
            notify_user("Houve um erro ao processar as entradas. Por favor, tente novamente mais tarde.")
            print(e)  # Apenas para depuração, pode ser removido em ambiente de produção


    @staticmethod
    def handle_other_state(user_states, chat_id, notify_user, message):
        # Lógica para outro estado de espera
        pass

    @staticmethod
    def handle_process_command(user_states, chat_id, notify_user, message=None):
        user_state = user_states.get(chat_id, {}).get('state')
        if user_state in Utils.estado_espera:
            handler = Utils.estado_espera[user_state]
            handler(user_states, chat_id, notify_user, message)
        else:
            # Lógica para outros estados ou nenhum estado específico
            pass

    estado_espera = {
        'Aguardando_links': handle_waiting_links,
        'Estado_erro': handle_other_state
    }


