import unittest
from config.setting_load import load_config  #


class TestLoadConfig(unittest.TestCase):

    def test_load_config_file_exists(self):
        # Testa se o arquivo de configuração pode ser carregado corretamente
        config = load_config()
        self.assertIsNotNone(config)

    def test_load_config_telegram_keys_exist(self):
        # Testa se as chaves necessárias para o Telegram existem no arquivo de configuração
        config = load_config()
        self.assertIn('telegram', config)
        self.assertIn('bot_token', config['telegram'])
        self.assertIn('chat_id', config['telegram'])

    def test_load_config_categorias_exist(self):
        # Testa se a seção 'categorias' existe no arquivo de configuração
        config = load_config()
        self.assertIn('categorias', config)

    def test_load_config_categoria1_valid(self):
        # Testa se a Categoria1 está presente e possui um link válido
        config = load_config()
        self.assertIn('Categoria1', config['categorias'])
        self.assertTrue(config['categorias']['Categoria1'].startswith('http'))
        # Adicione mais verificações conforme necessário para o formato do link, se desejar


if __name__ == '__main__':
    unittest.main()
