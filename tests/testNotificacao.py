import unittest
from unittest.mock import patch
from view import Notificacao

class TestNotificacao(unittest.TestCase):
    def setUp(self):
        self.bot_token = 'your_bot_token_here'
        self.chat_id = 'your_chat_id_here'
        self.notificacao = Notificacao(self.bot_token, self.chat_id)
        self.mensagem = "Exemplo de mensagem de notificação."

    @patch('requests.post')
    def test_enviar_mensagem(self, mock_post):
        # Simula a resposta da requisição POST
        mock_post.return_value.json.return_value = {'ok': True}

        # Chama o método enviar_mensagem
        self.notificacao.enviar_mensagem(self.mensagem)

        # Verifica se o método requests.post foi chamado com os parâmetros corretos
        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            data={'chat_id': self.chat_id, 'text': self.mensagem, 'parse_mode': 'HTML'}
        )

if __name__ == '__main__':
    unittest.main()
