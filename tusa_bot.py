import json
import requests
import datetime
import time
import NOdebts

token = '1183110811:AAGNJmL0YF_QfdlixXaAipFe1CkTyTy9ZoI'
way_to_tusapoints = 'tusapoints.txt'

proxies = {
  'http': 'socks5h://94.103.81.38:1088',
  'https': 'socks5h://94.103.81.38:1088',
}


class BotClass:

    def __init__(self, token, proxies):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.proxies = proxies

    def get_updates(self, offset=None, timeout=100):
        method = 'getUpdates'   # метод для получения обновлений через long polling
        params = {'timeout': timeout, 'offset': offset} # offset указывает id обновления начиная с которого их нужно получать
        resp = requests.get(self.api_url + method, params, proxies = self.proxies)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text, reply_markup=None):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        resp = requests.post(self.api_url + method, params, proxies = self.proxies)
        return resp

    def get_last_update(self, offset=None, timeout=100):
        get_result = self.get_updates(offset, timeout)

        if len(get_result) > 0: last_update = get_result[-1]
        else: last_update = None

        return last_update





tusabot = BotClass(token,proxies)

def main():
    offset = None
    now = datetime.datetime.now()
    today = now.day

    how_writing_new_tusapoint_id = set()
    how_writing_debts_id = set()

    while True:

# этот блок получает обновления от бота
# ------------------------------------------------------------------------------
        last_update = tusabot.get_last_update(offset)
        print(last_update)

        if last_update == None: continue

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
# ------------------------------------------------------------------------------
        if today == now.day and 9 <= now.hour < 18:
            tusabot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1


        if last_chat_text == '/new_tusapoint':
            tusabot.send_message(last_chat_id, 'Что у тебя?')
            how_writing_new_tusapoint_id.add(last_chat_id)

        elif last_chat_text == '/go_debts':
            tusabot.send_message(last_chat_id, 'Напиши, кто сколько потратил?\nНужна инфа в таком виде:')
            tusabot.send_message(last_chat_id, 'Чувак 1000\nЧувиха 200\nПарнишка 0\nДевчонка 0')
            how_writing_debts_id.add(last_chat_id)

        elif last_chat_text == '/get_list':
            tusabot.send_message(last_chat_id, 'Вот:')

            with open(way_to_tusapoints, 'r') as f:
                for s in f:
                    keyboard = json.dumps({'inline_keyboard': [[{'text': '🗑 delete', 'callback_data': 'delete_tusapoint'}]]})
                    tusabot.send_message(last_chat_id, s, keyboard)

        elif last_chat_text == 'delete_tusapoint':
            dtext = last_update['callback_query']['message']['text']+ '\n'
            data_from_file = []
            with open(way_to_tusapoints, 'r') as f:
                for s in f:
                    if s != dtext:
                        data_from_file.append(s)
            print(data_from_file)
            with open(way_to_tusapoints, 'w') as f:
                for s in data_from_file:
                    f.write( s )

            tusabot.send_message(last_chat_id, 'Стёр "'+dtext[:10]+'"...')

        elif last_chat_id in how_writing_debts_id:
            tusabot.send_message(last_chat_id, 'Вычисляю...')
            users = {}
            lst = last_chat_text.replace(' ', '\n').strip().split('\n')
            for i in range(0,len(lst),2): users[lst[i]]= int(lst[i+1])
            trans = NOdebts.equally(users)

            one_str = 'Вот список транзакций:\n'
            for i in trans:
                one_str += i+': '+ str(trans[i])+ '\n'
            tusabot.send_message(last_chat_id, one_str)



        elif last_chat_id in how_writing_new_tusapoint_id:
            with open(way_to_tusapoints, 'a') as f:
                f.write( last_chat_text + '\n')
                print(last_chat_text)
            tusabot.send_message(last_chat_id, 'Записал')
            how_writing_new_tusapoint_id.remove(last_chat_id)

        else:
            tusabot.send_message(last_chat_id, 'Что это?')


        offset = last_update_id + 1

if __name__ == '__main__':
    for i in range(5):
        try:
            main()
        except:
            print('except',i)
            time.sleep(5*(1+i))
    main()
