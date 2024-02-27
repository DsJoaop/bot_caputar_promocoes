from config.setting_load import get_lista_desejos


class CommandPichau:
    def __init__(self, states, user):
        self.user_states = states
        self.user = user

        def handle_list_desejos(self, chat_id):
            user_state = self.user_states.get(chat_id, {}).get('state')
            if user_state == 'liberado' or user_state is None:
                links = get_lista_desejos()
                if links is not None:
                    a = chat_id
                    # produtos = listar_produtos(links)
                    # self.notify_user.enviar_mensagem(formatar_mensagem(produtos))
                else:
                    self.notify_user.enviar_mensagem("Erro ao carregar lista de desejos")
            else:
                self.notify_user.enviar_mensagem("Termine o processo anterior para ver a lista de desejos!")

        def handle_add_list_desejos(self, chat_id):
            user_state = self.user_states.get(chat_id, {}).get('state')

            if user_state == 'liberado' or user_state is None:
                mensagem = (
                    "Envie os links e os preços máximos dos produtos que deseja adicionar à lista de desejos.\n\n"
                    "Envie uma linha para cada produto no formato:\n\n"
                    "`preço_maximo ; link_do_produto`\n\n"
                    "Aguardando suas mensagens..."
                )
                self.notify_user.enviar_mensagem(mensagem)
                self.user_states[chat_id]['state'] = 'Aguardando_links'
            else:
                self.notify_user.enviar_mensagem("Termine o processo anterior para ver a lista de desejos!")

        def handle_waiting_links(self, user_states, chat_id, notify_user, data):
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
                            notify_user.enviar_mensagem(
                                "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha.")
                            user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto
                            return
                        except Exception as e:
                            print(e)
                            notify_user.enviar_mensagem(
                                "Houve um erro ao salvar os produtos desejados. Por favor, tente novamente mais tarde.")
                            user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto
                            return

                user_states[chat_id]['state'] = None  # Reinicia o estado após adicionar o produto

                if produtos_adicionados:
                    for link, preco in produtos_adicionados:
                        notify_user.enviar_mensagem(
                            f"O produto no link: {link} \n\nFoi adicionado à lista de desejos com um preço máximo de {preco}.")
                else:
                    notify_user(
                        "Por favor, envie o preço seguido pelo link do produto separados por ';' em cada linha.")
            except Exception as e:
                notify_user.enviar_mensagem(
                    "Houve um erro ao processar as entradas. Por favor, tente novamente mais tarde.")
                print(e)  # Apenas para depuração, pode ser removido em ambiente de produção