from config.setting_load import get_lista_desejos, add_produto_desejo
from src.core_products.controller_monitor import ControllerMonitor
from src.data_acess.data_pichau import formatar_mensagem, listar_produtos

controller = ControllerMonitor()


def command_start(user_states, chat_id, notify_user, message=None):
    user_state = user_states.get(chat_id, {}).get('state')
    if user_state == 'liberado' or user_state is None:
        welcome_message = (
            "Bem-vindo ao bot de monitoramento de preços! 🌟\n"
            "Digite /help para ver os comandos disponíveis."
        )
        controller.iniciar_monitoramento()
        notify_user(welcome_message)
    else:
        notify_user("Termine o processo anterior para ver o comando!")


def command_stop(user_states, chat_id, notify_user, message=None):
    user_states[chat_id]['state'] = 'stop'
    controller.parar_monitoramento()
    bye_message = "Monitoramento pausado. Até logo!"
    notify_user(bye_message)


def command_help(user_states, chat_id, notify_user, message=None):
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


def command_list_desejos(user_states, chat_id, notify_user, message=None):
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


def command_add_list_desejos(user_states, chat_id, notify_user, message):
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


def other_command(user_states, chat_id, notify_user, message):
    # Lógica para outro estado de espera
    pass


def command_process(user_states, chat_id, notify_user, message=None):
    user_state = user_states.get(chat_id, {}).get('state')
    if user_state in estado_espera:
        handler = estado_espera[user_state]
        handler(user_states, chat_id, notify_user, message)
    else:
        notify_user("Estado de espera indefinido")


estado_espera = {
    'Aguardando_links': handle_waiting_links,
    'Estado_erro': other_command
}
