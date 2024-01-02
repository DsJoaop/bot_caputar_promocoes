import requests


def send_mensage(mensagem, reply_markup=None):
    dados = {
        'chat_id': "2145296654",
        'text': mensagem,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        dados['reply_markup'] = reply_markup

    url = f"https://api.telegram.org/bot6474525795:AAE0REuCbl_4kxPL67IZKNAyZ-Kp1iOlYzg/sendMessage"
    try:
        response = requests.post(url, json=dados)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print("Falha ao enviar mensagem")
    except requests.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")