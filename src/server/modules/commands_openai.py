import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta


class CommandOpenai:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.config_file = None
        self.limits = self.load_limits()

    def load_limits(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        assets_directory = os.path.abspath(os.path.join(parent_directory, '..', '..', 'config'))
        file_path = os.path.join(assets_directory, 'limits_config.json')
        self.config_file = file_path

        if os.path.exists(file_path):
            with open(file_path, 'r') as config_file:
                return json.load(config_file)
        else:
            print("Limites não carregados")
            return {
                'rpm': {'limit': 3, 'count': 0, 'last_reset': str(datetime.now())},
                'rpd': {'limit': 200, 'count': 0, 'last_reset': str(datetime.now())},
                'tpm': {'limit': 40000, 'count': 0, 'last_reset': str(datetime.now())}
            }

    def save_limits(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.limits, file, indent=4)

    def check_limits(self):
        self.check_reset_time()
        for limit_type, limit_data in self.limits.items():
            if limit_data['count'] >= limit_data['limit']:
                return f"{limit_type.upper()} limite excedido."

    def check_reset_time(self):
        current_time = datetime.now()
        for limit_type, limit_data in self.limits.items():
            last_reset_time = datetime.fromisoformat(limit_data['last_reset'])
            if current_time - last_reset_time > self.get_reset_interval(limit_type):
                limit_data['count'] = 0
                limit_data['last_reset'] = str(current_time)

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
            max_tokens=256,
            messages=[
                {"role": "system",
                 "content": "Deve responder com sarcasmo, ironia e de forma ríspida. Seja sucinto"},
                {"role": "user", "content": message}
            ]
        )
        for limit_data in self.limits.values():
            limit_data['count'] += 1
        self.save_limits()
        return completion.choices[0].message.content


def main():
    openai_command = CommandOpenai()
    user_input = input("Digite sua mensagem: ")
    response = openai_command.generate_response(user_input)
    print("Resposta do modelo:", response)


if __name__ == "__main__":
    main()
