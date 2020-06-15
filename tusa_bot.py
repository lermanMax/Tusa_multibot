# -*- coding: utf-8 -*-

import json
import requests
import datetime

token = '1183110811:AAGNJmL0YF_QfdlixXaAipFe1CkTyTy9ZoI'
way_to_tusapoints = 'data/tusapoints.txt'

class BotClass:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=1000):
        method = 'getUpdates'   # метод для получения обновлений через long polling
        params = {'timeout': timeout, 'offset': offset} # offset указывает id обновления начиная с которого их нужно получать
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text, keyboard=None):
        method = 'sendMessage'
        reply_markup = json.dumps(keyboard)
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self, offset=None, timeout=1000):
        get_result = self.get_updates(offset, timeout)

        if len(get_result) > 0: last_update = get_result[-1]
        else: last_update = None

        return last_update





tusabot = BotClass(token)

def main():
    offset = None
    now = datetime.datetime.now()
    today = now.day

    how_writing_new_tusapoint_id = set()

    while True:

# этот блок получает обновления от бота
# -----------------------------------------------------------------------------

        last_update = tusabot.get_last_update(offset)
        print(last_update)

        last_update_id = last_update['update_id']

        if 'message' in last_update:
            last_chat_id = last_update['message']['from']['id']
            last_chat_text = last_update['message']['text']
            last_chat_name = last_update['message']['from']['first_name']

        elif 'callback_query' in last_update:
            last_chat_id = last_update['callback_query']['from']['id']
            last_chat_text = last_update['callback_query']['data']
            last_chat_name = last_update['callback_query']['from']['first_name']

        else:
            last_chat_text = None
            last_chat_id = None
            last_chat_name = None

        print(last_chat_text)

# логика бота
# -----------------------------------------------------------------------------
        if today == now.day and 9 <= now.hour < 18:
            tusabot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1


        if last_chat_text == '/new_tusapoint':
            tusabot.send_message(last_chat_id, 'Что у тебя?')
            how_writing_new_tusapoint_id.add(last_chat_id)

        elif last_chat_text == '/get_list':
            tusabot.send_message(last_chat_id, 'Вот:')

            with open(way_to_tusapoints, 'r') as f:
                for s in f:
                    keyboard = {'inline_keyboard': [[{'text': '🗑 delete', 'callback_data': 'delete_tusapoint'}]]}
                    tusabot.send_message(last_chat_id, s, keyboard)

        elif last_chat_text == 'delete_tusapoint':
            dtext = last_update['callback_query']['message']['text']+ '\n'
            data_from_file = []
            with open(way_to_tusapoints, 'r') as f:
                for s in f:
                    if s != dtext:
                        data_from_file.append(s)
            with open(way_to_tusapoints, 'w') as f:
                for s in data_from_file:
                    f.write( s )
            tusabot.send_message(last_chat_id, 'Стёр')

        elif last_chat_id in how_writing_new_tusapoint_id:
            with open(way_to_tusapoints, 'a') as f:
                f.write( last_chat_text + '\n')
            tusabot.send_message(last_chat_id, 'Записал')
            how_writing_new_tusapoint_id.remove(last_chat_id)

        else:
            tusabot.send_message(last_chat_id, 'Что это?')


        offset = last_update_id + 1

if __name__ == '__main__':
  # main()
  while True:
      try:
        main()
      except:
        time.sleep(5)
