import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.config.setting_load import load_config
from src.bot_iteration.telegram_notify import Notificacao


class TestNotificacao(unittest.TestCase):
    def setUp(self):
        config = load_config()
        if config:
            telegram_config = config.get('telegram')
            self.bot_token = telegram_config.get('bot_token')
            self.chat_id = telegram_config.get('chat_id')
            self.notificacao = Notificacao(self.bot_token, self.chat_id)
            self.mensagem = "Exemplo de mensagem de notificação."
        else:
            self.bot_token = None
            self.chat_id = None
            self.notificacao = None
            self.mensagem = None

    @patch('requests.post')
    def test_enviar_mensagem(self, mock_post):
        if not self.bot_token or not self.chat_id or not self.notificacao:
            self.skipTest("Configuração ausente. Não é possível realizar o teste.")

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
