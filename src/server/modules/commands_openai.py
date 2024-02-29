import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta

class CommandOpenai:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.limits = {
            'rpm': {'limit': 3, 'count': 0, 'last_reset': datetime.now()},
            'rpd': {'limit': 200, 'count': 0, 'last_reset': datetime.now()},
            'tpm': {'limit': 40000, 'count': 0, 'last_reset': datetime.now()}
        }

    def check_limits(self):
        self.check_reset_time()
        for limit_type, limit_data in self.limits.items():
            if limit_data['count'] >= limit_data['limit']:
                return f"{limit_type.upper()} limite excedido."

    def check_reset_time(self):
        current_time = datetime.now()
        for limit_type, limit_data in self.limits.items():
            if current_time - limit_data['last_reset'] > self.get_reset_interval(limit_type):
                limit_data['count'] = 0
                limit_data['last_reset'] = current_time

    def get_reset_interval(self, limit_type):
        if limit_type == 'rpm':
            return timedelta(minutes=1)
        elif limit_type == 'rpd':
            return timedelta(days=1)
        elif limit_type == 'tpm':
            return timedelta(days=30)

    def generate_response(self, message):
        self.check_limits()
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Oh, que surpresa! Outro comando que não consegui encontrar."
                            " Você deve ser tão inovador."},
                {"role": "user", "content": message}
            ]
        )
        for limit_data in self.limits.values():
            limit_data['count'] += 1
        return completion.choices[0].message


def main():
    openai_command = CommandOpenai()
    user_input = input("Digite sua mensagem: ")
    response = openai_command.generate_response(user_input)
    print("Resposta do modelo:", response)



if __name__ == "__main__":
    main()
