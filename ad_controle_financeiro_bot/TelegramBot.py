import json
import os

import requests
from dotenv import load_dotenv

from data.DriveBot import DriveBot
from data.TransformDataframe import transform_dataframe
from visualization.DataVisualization import vertial_bar_nps_mean, hist_nps

load_dotenv()


class TelegramBot:
    def __init__(self):
        token = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{token}/"
        self.driveBot = DriveBot()

    def start(self):
        update_id = None
        while True:
            update = self.get_message(update_id)
            messages = update["result"]
            if messages:
                for message in messages:
                    try:
                        update_id = message["update_id"]
                        chat_id = message["message"]["from"]["id"]
                        message_text = message["message"]["text"]
                        answer_bot, answer_bool = self.create_answer(message_text)
                        self.send_answer(chat_id, answer_bot, answer_bool)
                    except:
                        print("ocorreu um erro")

    def get_message(self, update_id):
        link_request = f"{self.url}getUpdates?timeout=1000"

        if update_id:
            link_request = f"{self.url}getUpdates?timeout=1000&offset={update_id + 1}"

        result = requests.get(link_request)
        return json.loads(result.content)

    def create_answer(self, message_text):
        dataframe = transform_dataframe(self.driveBot.get_sheet_data())

        if message_text in ["oi", "Oi", "ola", "Ola", "."]:
            return (
                """Olá, tudo bem? Bem-vindo ao Bot do RH\n 1 - Para verificar o NPS médio por Setor\n 2 - Para verificar o NPS médio por Contratação\n 3 - Para verificar a distribuição do NPS Interno\n""",
                0,
            )
        elif message_text == "1":
            return vertial_bar_nps_mean(dataframe, "Setor"), 1
        elif message_text == "2":
            return vertial_bar_nps_mean(dataframe, "Tipo de Contratação"), 1
        elif message_text == "3":
            return hist_nps(dataframe), 1
        else:
            return (
                """Não entendi... por favor, selecione uma das opções válidas\n 1 - Para verificar o NPS médio por Setor\n 2 - Para verificar o NPS médio por Contratação\n 3 - Para verificar a distribuição do NPS Interno\n""",
                0,
            )

    def send_answer(self, chat_id, answer, answer_bool):
        if answer_bool == 0:
            link_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
            requests.get(link_send)
            return
        else:
            figure = r"D:\Dev\python\ad-controle-financeiro-bot\graph_last_fig.png"
            file = {"photo": open(figure, "rb")}
            link_send = f"{self.url}sendPhoto?chat_id={chat_id}"
            requests.post(link_send, files=file)
