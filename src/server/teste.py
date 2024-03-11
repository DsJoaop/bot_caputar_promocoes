import asyncio
import os
import aiohttp

from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel


load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


class Mensagem(BaseModel):
    chat_id: int
    text: str


class TelegramBot(FastAPI, aiohttp.ClientSession):
    def __init__(self):
        super().__init__()

        # Cria uma sessão HTTP assíncrona
        self._session = aiohttp.ClientSession()

        @self.post("/start")
        async def start(mensagem: Mensagem = Body(...)):
            if mensagem.text != "/start":
                raise HTTPException(status_code=400)

            resposta = f"Olá! \n\nUse /help para ver os comandos disponíveis."
            await enviar_mensagem(mensagem.chat_id, resposta)

        async def inicio(self):
            # Adicione o código que você deseja executar quando o bot for iniciado
            print("Bot iniciado!")

        @self.post("/stop")
        async def stop(mensagem: Mensagem = Body(...)):
            if mensagem.text != "/stop":
                raise HTTPException(status_code=400)

            resposta = "Tchau! \n\nVolte sempre que quiser!"
            await enviar_mensagem(mensagem.chat_id, resposta)

        @self.post("/help")
        async def help(mensagem: Mensagem = Body(...)):
            if mensagem.text != "/help":
                raise HTTPException(status_code=400)

            resposta = f"""
            **Comandos disponíveis:**

            /start - Inicia o bot e exibe uma mensagem de boas-vindas.
            /stop - Encerra a conversa com o bot.
            /help - Exibe esta lista de comandos.
            """
            await enviar_mensagem(mensagem.chat_id, resposta)

        async def enviar_mensagem(chat_id: int, texto: str):
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_id, "text": texto}

            async with self._session.post(url, json=data) as resposta:
                if resposta.status != 200:
                    raise HTTPException(status_code=500)


async def main():
    app = TelegramBot()

    # Inicia a sessão HTTP
    await app._session.__aenter__()

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        # Fecha a sessão HTTP
        await app._session.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main())
