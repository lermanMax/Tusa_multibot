import json
import requests
import datetime
import time
import NOdebts
import BotClass
import click

token = '1183110811:AAGNJmL0YF_QfdlixXaAipFe1CkTyTy9ZoI'
way_to_tusapoints = 'tusapoints.txt'

socks = {
  'http': 'socks5h://94.103.81.38:1088',
  'https': 'socks5h://94.103.81.38:1088',
}

def new_tusapoint(text, base):
    with open(base, 'a') as f:
        f.write( text + '\n')
        print(text)
    return

def delete_tusapoint(text, base):
    data_from_file = []
    with open(base, 'r') as f:
        for s in f:
            if s != text: data_from_file.append(s)
    print(data_from_file)
    with open(base, 'w') as f:
        for s in data_from_file:
            f.write( s )
    return

def get_list(base):
    list = []
    with open(base, 'r') as f:
        for s in f: list.append(s)
    return list

@click.command()
@click.argument('proxies_on')
def main(proxies_on):
    proxies = None
    if proxies_on =='yes': proxies = socks
    tusabot = BotClass.BotClass(token,proxies)

    offset = None
    now = datetime.datetime.now()
    today = now.day

    how_writing_new_tusapoint_id = set()
    how_writing_debts_id = set()
    how_saw_hello = set()

    last_command_from_user = {}

    while True:
# этот блок получает обновления от бота
# ------------------------------------------------------------------------------
        last_update = tusabot.get_last_update(offset)
        print(last_update)

        if last_update == None: continue # ждать обновлений

        last_update_id = last_update['update_id']

        if 'message' in last_update:
            last_chat_id = last_update['message']['from']['id']
            last_chat_name = last_update['message']['from']['first_name']
            if 'text' in last_update['message']:
                last_chat_text = last_update['message']['text']
            else: # не реагировать на сообщения кроме текстовых
                last_chat_text = None
                continue

        elif 'callback_query' in last_update:
            last_chat_id = last_update['callback_query']['from']['id']
            last_chat_text = last_update['callback_query']['data']
            last_chat_name = last_update['callback_query']['from']['first_name']

        else:
            last_chat_text = None
            last_chat_id = None
            last_chat_name = None

        print(last_chat_text)

        if last_chat_id not in last_command_from_user:
            last_command_from_user[last_chat_id] = None  
# логика бота
# ------------------------------------------------------------------------------
        if today == now.day and 5 <= now.hour < 6:
            how_saw_hello.clear()
            today += 1
        if last_chat_id not in how_saw_hello:
            tusabot.send_message(last_chat_id, 'Приветствую, {}. Для чего я создан?'.format(last_chat_name))
            how_saw_hello.add(last_chat_id)


        if last_chat_text == '/new_tusapoint':
            tusabot.send_message(last_chat_id, 'Что у тебя?')
            how_writing_new_tusapoint_id.add(last_chat_id)
            last_command_from_user[last_chat_id] = '/new_tusapoint'

        elif last_chat_text == '/go_debts':
            tusabot.send_message(last_chat_id, 'Напиши, кто сколько потратил?\nНужна инфа в таком виде:')
            tusabot.send_message(last_chat_id, 'Чувак 1000\nЧувиха 200\nПарнишка 0\nДевчонка 0')
            how_writing_debts_id.add(last_chat_id)
            last_command_from_user[last_chat_id] = '/go_debts'

        elif last_chat_text == '/get_list':
            tusabot.send_message(last_chat_id, 'Вот:')
            keyboard = json.dumps({'inline_keyboard': [[{'text': '🗑 delete', 'callback_data': 'delete_tusapoint'}]]})
            list_tusapoints = get_list(way_to_tusapoints)
            for i in list_tusapoints: tusabot.send_message(last_chat_id, i, keyboard)

        elif last_chat_text == 'delete_tusapoint':
            dtext = last_update['callback_query']['message']['text']+ '\n'
            delete_tusapoint(dtext, way_to_tusapoints)
            tusabot.send_message(last_chat_id, 'Стёр: '+dtext[:10].strip()+'...')

        # elif last_chat_id in how_writing_debts_id:
        elif last_command_from_user[last_chat_id] == '/go_debts':
            tusabot.send_message(last_chat_id, 'Вычисляю...')

            try:
                #библиотека участников с вложенной ими суммой
                users = {}
                lst = last_chat_text.replace(' ', '\n').strip().split('\n')
                for i in range(0,len(lst),2): users[lst[i]]= int(lst[i+1])
                #вычисления для этой библиотеки
                trans = NOdebts.equally(users)
                # формирование ответа
                one_str = 'Вот список транзакций:\n'
                for i in trans:
                    one_str += i+': '+ str(trans[i])+ '\n'
                tusabot.send_message(last_chat_id, one_str)
            except:
                tusabot.send_message(last_chat_id, 'Херовые данные чет')

            how_writing_debts_id.remove(last_chat_id)
            last_command_from_user[last_chat_id] = None


        # elif last_chat_id in how_writing_new_tusapoint_id:
        elif last_command_from_user[last_chat_id] == '/new_tusapoint':
            new_tusapoint(last_chat_text, way_to_tusapoints)
            tusabot.send_message(last_chat_id, 'Записал')
            how_writing_new_tusapoint_id.remove(last_chat_id)
            last_command_from_user[last_chat_id] = None

        else:
            tusabot.send_message(last_chat_id, 'Что это?')


        offset = last_update_id + 1


if __name__ == '__main__':
    for i in range(5):
        try:
            main()
        except:
            print('except',i)
            time.sleep(15)

    # # tusabot.send_message(98244574, 'Силы покидают меня...')
    main()
