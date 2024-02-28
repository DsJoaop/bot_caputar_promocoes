import os
from dotenv import load_dotenv
from openai import OpenAI


class CommandOpenai:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, message, comando_nao_encontrado=False):
        if comando_nao_encontrado:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Oh, que surpresa! Outro comando que não consegui encontrar."
                                " Você deve ser tão inovador."},
                    {"role": "user", "content": message}
                ]
            )
        else:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Você é um assistente poético, habilidoso em explicar conceitos de programação complexos"
                                " com estilo criativo."},
                    {"role": "user", "content": message}
                ]
            )

        return completion.choices[0].message
