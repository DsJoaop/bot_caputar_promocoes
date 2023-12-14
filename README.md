# Monitor de Preços

Este é um projeto Python para monitoramento de preços. Realiza scraping de websites para acompanhar e notificar mudanças nos preços de produtos em diferentes categorias.

## Funcionalidades

- **Scraping de Preços:** Coleta informações sobre produtos e preços em sites especificados.
- **Monitoramento Contínuo:** Acompanha regularmente os preços e compara com valores anteriores para detectar alterações significativas.
- **Notificações:** Envia notificações sobre mudanças relevantes nos preços, por exemplo, via Telegram ou e-mail.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/monitor-precos.git
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Configuração

1. Configure as informações necessárias no arquivo `config.json` conforme o exemplo fornecido em `config_example.json`.
2. Verifique se as dependências estão instaladas corretamente.

## Uso

Execute o programa usando o seguinte comando:

   
    python controller.py
   

Isso iniciará o monitoramento com base nas configurações fornecidas no arquivo `config.json`.

## Estrutura do Projeto

- **`model.py`:** Contém classes relacionadas aos dados e à lógica de scraping.
- **`view.py`:** Classes responsáveis por notificações e logs.
- **`controller.py`:** O controlador principal que coordena a execução do monitoramento de preços.