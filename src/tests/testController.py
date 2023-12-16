import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.core.controller import Controller  # Importe sua classe Controller aqui

# Dados de configuração fornecidos
config_data = {
    "telegram": {
        "bot_token": "6474525795:AAE0REuCbl_4kxPL67IZKNAyZ-Kp1iOlYzg",
        "chat_id": "2145296654"
    },
    "categorias": {
        "Categoria1": "https://www.pichau.com.br/hardware/placa-m-e"
    }
}


class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    def test_main_with_valid_config(self):
        # Mocking necessary components
        mock_load_config = MagicMock(return_value=config_data)
        self.controller.logger.log_error = MagicMock()
        self.controller.monitorar_precos = MagicMock()

        # Patching the load_config method to return our mock value
        with patch('src.config.setting_load.load_config', mock_load_config):
            self.controller.main()

        mock_load_config.assert_called_once()
        self.assertFalse(self.controller.logger.log_error.called)
        self.assertTrue(self.controller.monitorar_precos.called)

    def test_main_with_invalid_config(self):
        # Mocking necessary components
        mock_load_config = MagicMock(return_value=None)
        self.controller.logger.log_error = MagicMock()

        # Patching the load_config method to return our mock value
        with patch('src.config.setting_load.load_config', mock_load_config):
            self.controller.main()

        mock_load_config.assert_called_once()
        self.assertTrue(self.controller.logger.log_error.called)
        self.assertFalse(self.controller.monitorar_precos.called)

    # You can add more test cases for other methods if needed


if __name__ == '__main__':
    unittest.main()
