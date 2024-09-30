# Monitor de Preços

Este é um projeto Python para monitoramento de preços. Realiza scraping de websites para acompanhar e notificar mudanças nos preços de produtos em diferentes categorias.

## Funcionalidades

- **Scraping de Preços:** Coleta informações sobre produtos e preços em sites especificados.
- **Monitoramento Contínuo:** Acompanha regularmente os preços e compara com valores anteriores para detectar alterações significativas.
- **Notificações:** Envia notificações sobre mudanças relevantes nos preços, por exemplo, via Telegram ou e-mail.

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

Para iniciar o monitoramento de preços, execute:

```bash
python src/core/mainController.py
