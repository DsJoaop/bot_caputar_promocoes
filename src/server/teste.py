from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import asyncio

app = FastAPI()

TELEGRAM_BOT_TOKEN = "6474525795:AAE0REuCbl_4kxPL67IZKNAyZ-Kp1iOlYzg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"


class Update(BaseModel):
    update_id: int
    message: dict


@app.post("/start")
async def start_command(update: Update):
    message = update.message
    chat_id = message["chat"]["id"]
    await send_message(chat_id, "Welcome to the bot!")


@app.post("/help")
async def help_command(update: Update):
    message = update.message
    chat_id = message["chat"]["id"]
    await send_message(chat_id, "This is a help message.")


@app.post("/stop")
async def stop_command(update: Update):
    message = update.message
    chat_id = message["chat"]["id"]
    await send_message(chat_id, "Stopping the bot.")
    # You can add additional logic here for stopping the bot or removing it from the chat


async def send_message(chat_id: int, text: str):
    url = f"{TELEGRAM_API_URL}sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)