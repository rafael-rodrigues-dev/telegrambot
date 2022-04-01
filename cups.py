import requests
import emoji
import pandas as pd
from time import sleep


class Cup:
    def __init__(self, id, name):
        self.competition_id = id
        self.name = name
        self.list_results = list()
        self.token = '5160616287:AAE8BkOSoaYHVvkAedU4OK8_Zav669NuWDg'

    def response(self, url, data):
        self.url = url
        self.data = data
        self.data['variables']['competitionId'] = self.competition_id
        self.result = requests.post(self.url, json=self.data).json()

        return self.extract_data(self.result)


    def extract_data(self, info):
        self.info = info

        matches = self.info['data']['matchesByCompetition']['matches']

        for match in matches:
            time = float(match['name'][:5])
            home = match['teamA']['finalScore']
            away = match['teamB']['finalScore']
            final_score = f'{home} X {away}'

            if home + away >= 3:
                over25 = 'Sim'
            else:
                over25 = 'Nao'

            if home and away > 0:
                both_scores = 'Sim'
            else:
                both_scores = 'Não'

            self.list_results.append(
                [time, match['name'][6:], final_score, over25, both_scores])

        df = pd.DataFrame(self.list_results, columns=(
            'Horário', 'Partida', 'Resultado', 'Over 2.5', 'Ambas Marcam'))
        self.resultado_final = [self.list_results[0],
                                self.list_results[1], self.list_results[2]]

        print(df)

        self.hour1 = str(self.list_results[18][0]).split('.')
        self.hour2 = int(self.hour1[0]) + 1

        if self.hour2 > 24:
            self.hour2 -= 24

        self.minute1 = int(self.hour1[1])
        self.minute2 = int(self.hour1[1]) + 3
        self.minute3 = int(self.hour1[1]) + 6

        if self.minute1 >= 60:
            self.minute1 -= 60

        if self.minute2 >= 60:
            self.minute2 -= 60

        if self.minute3 >= 60:
            self.minute3 -= 60

        self.circle = ':red_circle: OVER 2.5 :red_circle:'

        return self.verify()

    def verify(self):
        if self.list_results[18][2] == '1 X 1':
            self.circle = ':purple_circle: AMBAS MARCAM :purple_circle:'
            self.send_message()
            self.edit_ambas(self.message_id)

        if self.list_results[18][2] == '1 X 2':
            self.send_message()
            self.edit_over(self.message_id)

    def send_message(self):
        self.message = emoji.emojize(
            f':soccer_ball: {self.name} :soccer_ball: \n :alarm_clock: {self.hour2} :alarm_clock: \n :hourglass_done:{self.minute1} - {self.minute2} - {self.minute3}:hourglass_done: \n {self.circle}')
        telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id=@reidovirtualsite&text={self.message}'
        self.r = requests.post(telegram_url)
        self.info = self.r.json()
        self.message_id = int(self.info['result']['message_id'])
        print(self.message_id)
        print('MENSAGEM ENVIADA')

    def edit_ambas(self, id: int):
        sleep(300)
        self.new_request = requests.post(self.url, json=self.data)
        self.updated_result = self.new_request.json()
        self.extract_data(self.updated_result)
        if self.resultado_final[0][4] == 'Sim' or self.resultado_final[1][4] == 'Sim' or self.resultado_final[2][4] == 'Sim':
            self.edited_message = f'{self.message} \n' + \
                emoji.emojize(':check_mark_button:') * 5
            telegram_url_edit = f'https://api.telegram.org/bot{self.token}/editMessageText?chat_id=@reidovirtualsite&text={self.edited_message}&message_id={id}'
            requests.post(telegram_url_edit)
            print(self.edited_message)
            print('MENSAGEM EDITADA')

        else:
            self.edited_message = f'{self.message} \n' + \
                emoji.emojize(':cross_mark:') * 5
            telegram_url_edit = f'https://api.telegram.org/bot{self.token}/editMessageText?chat_id=@reidovirtualsite&text={self.edited_message}&message_id={id}'
            requests.post(telegram_url_edit)
            print(self.edited_message)
            print('MENSAGEM EDITADA')

    def edit_over(self, id: int):
        sleep(300)
        self.new_request = requests.post(self.url, json=self.data)
        self.updated_result = self.new_request.json()
        self.extract_data(self.updated_result)
        if self.resultado_final[0][3] == 'Sim' or self.resultado_final[1][3] == 'Sim' or self.resultado_final[2][3] == 'Sim':
            self.edited_message = f'{self.message} \n' + emoji.emojize(':check_mark_button:') * 5
            telegram_url_edit = f'https://api.telegram.org/bot{self.token}/editMessageText?chat_id=@reidovirtualsite&text={self.edited_message}&message_id={id}'
            requests.post(telegram_url_edit)
            print(self.edited_message)
            print('MENSAGEM EDITADA')

        else:
            self.edited_message = f'{self.message} \n' + emoji.emojize(':cross_mark:') * 5
            telegram_url_edit = f'https://api.telegram.org/bot{self.token}/editMessageText?chat_id=@reidovirtualsite&text={self.edited_message}&message_id={id}'
            requests.post(telegram_url_edit)
            print(self.edited_message)
            print('MENSAGEM EDITADA')
