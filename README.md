# Monitor de Preços

Este é um projeto Python para monitoramento de preços. Realiza scraping de websites para acompanhar e notificar mudanças nos preços de produtos em diferentes categorias.

## Funcionalidades

- **Scraping de Preços:** Coleta informações sobre produtos e preços em sites especificados.
- **Monitoramento Contínuo:** Acompanha regularmente os preços e compara com valores anteriores para detectar alterações significativas.
- **Notificações:** Envia notificações sobre mudanças relevantes nos preços, por exemplo, via Telegram ou e-mail.

## Estrutura de Diretórios

```json
├── src
│   ├── bot_iteration
│   │   └── telegram_notify.py
│   ├── config
│   │   ├── settings.json
│   │   └── setting_load.py
│   ├── core
│   │   ├── mainController.py
│   │   └── monitorCategory.py
│   ├── data_acess
│   │   ├── extractData.py
│   │   └── extractPay.py
│   └── model
│       └── produto.py
├── readme.md
└── requirements.txt
```

## Descrição

Este projeto é um sistema de monitoramento de preços que utiliza web scraping para rastrear e notificar sobre descontos em produtos de várias categorias.

## Pré-requisitos

- Python 3.x instalado
- Conexão à internet

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu_usuario/seu_projeto.git
    cd seu_projeto
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Configuração

1. Crie um arquivo `settings.json` no diretório `src/config` com a seguinte estrutura:

    ```json
    {
      "telegram": {
        "bot_token": "SEU_TOKEN_AQUI",
        "chat_id": "SEU_CHAT_ID_AQUI"
      },
      "categorias": {
        "Categoria1": "URL_DA_CATEGORIA_1",
        "Categoria2": "URL_DA_CATEGORIA_2"
      }
    }
    ```

    Substitua `"SEU_TOKEN_AQUI"` pelo token do seu bot no Telegram e `"SEU_CHAT_ID_AQUI"` pelo ID do chat onde as notificações serão enviadas. Adicione quantas categorias forem necessárias.

## Uso

Para iniciar o monitoramento de preços, execute:

```bash
python src/core/mainController.py