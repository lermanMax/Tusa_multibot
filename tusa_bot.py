import json
import datetime
import time
import MyTelegramBotLib
import NOdebts
import DB_tusabot
import click


token = '1183110811:AAGNJmL0YF_QfdlixXaAipFe1CkTyTy9ZoI'

socks = {
  'http': 'socks5h://94.103.81.38:1088',
  'https': 'socks5h://94.103.81.38:1088',
  }

DB_HOST = "localhost"
DB_NAME = "Tusa_db"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_PORT = "5432"    


@click.command()
@click.argument('proxies_on')
def start_tusabot(proxies_on = 'no'):
    proxies = None
    if proxies_on =='yes': proxies = socks
    
    tusabot = MyTelegramBotLib.BotClass(token,proxies)
    DB = DB_tusabot.DB_tusabot(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)

    today = datetime.datetime.now().day
    
    last_command = {} # key = chat id, value = last user's command 
    how_saw_hello = set()
    
    offset = None
    last_update = None
    
    
    while True:
        try:            
            while True:
        # ------------------------------------------------------------------------------
        # этот блок получает обновления от бота
                
                last_update = tusabot.get_last_update(offset)
                print(last_update)
        
                if last_update == None: continue
        
                last_update_id = last_update['update_id']
        
                if 'message' in last_update:
                    last_chat_id = last_update['message']['from']['id']
                    last_chat_text = last_update['message'].get('text')
        
                    last_chat_name = last_update['message']['from']['first_name']
        
                elif 'callback_query' in last_update:
                    last_chat_id = last_update['callback_query']['from']['id']
                    last_message_id = last_update['callback_query']['message']['message_id']
                    
                    data = last_update['callback_query']['data'].split(' ')
                    print(data)
                    if data[0] == 'tusapoints':
                        last_chat_text = data[1]
                    elif data[0] == 'tusapoint':
                        last_chat_text = data[1]
                        tusapoint_id = int(data[2])
        
                    last_chat_name = last_update['callback_query']['from']['first_name']
        
                else:
                    last_chat_text = None
                    last_chat_id = None
                    last_chat_name = None
        
                print(last_chat_text)
        
        # ------------------------------------------------------------------------------
        # логика бота
                
                if today == datetime.datetime.now().day and 5 <= datetime.datetime.now().hour < 6:
                    how_saw_hello.clear()
                    today += 1
        
                if last_chat_id not in how_saw_hello:
                    tusabot.send_message(last_chat_id, 'Приветствую, {}. Для чего я создан?'.format(last_chat_name))
                    how_saw_hello.add(last_chat_id)
        
        
                if last_chat_text == '/new_tusapoint':
                    tusabot.send_message(last_chat_id, 'Что у тебя?')
                    last_command[last_chat_id] = '/new_tusapoint'
        
                elif last_chat_text == '/go_debts':
                    tusabot.send_message(last_chat_id, 'Напиши, кто сколько потратил?\nНужна инфа в таком виде:')
                    tusabot.send_message(last_chat_id, 'Чувак 1000\nЧувиха 200\nПарнишка 0\nДевчонка 0')
                    last_command[last_chat_id] = '/go_debts'
        
                elif last_chat_text == '/get_list' or last_chat_text == 'update_list_of_tusapoints':
                    one_str = 'Вот список тусапоинтов:\n'
                    tusapoints = DB.get_tusapoint()
                    for row in tusapoints:
                        one_str +='◾' + row['description'] +' ♥'+ str(len(DB.get_like(row['id'])))+ '\n'
                    keyboard = json.dumps({'inline_keyboard': [[
                            {'text': '✏ edit', 'callback_data': 'tusapoints edit_list_of_tusapoints' },
                            {'text': '🔄 update', 'callback_data': 'tusapoints update_list_of_tusapoints' },                  
                            ]]})
            
                    if last_chat_text == '/get_list':
                        tusabot.send_message(last_chat_id, one_str, keyboard)
                    else:
                        tusabot.edit_message(last_chat_id, last_message_id, one_str, keyboard)
                        
                    last_command[last_chat_id] = None
                        
                    
                elif last_chat_text == 'edit_list_of_tusapoints':
                    
                    tusapoints = DB.get_tusapoint()
                    for row in tusapoints:
                        heart = '♥'
                        if not DB.get_like(row['id'], DB.get_friend(telegram_id = last_chat_id)['id']): heart = '🤍' 
                                            
                        keyboard = json.dumps({'inline_keyboard': [[
                                {'text': '🗑 del', 'callback_data': 'tusapoint delete_tusapoint '+str(row['id'])},
                                {'text': heart, 'callback_data': 'tusapoint like_tusapoint '+str(row['id'])}
                                ]]})
                        tusabot.send_message(last_chat_id, row['description'] + '\n' + '🖋author: '+DB.get_friend(row['author_id'])['name'], keyboard)
                    
        
                elif last_chat_text == 'delete_tusapoint':
                    description_13 = DB.get_tusapoint(t_id = tusapoint_id)['description']
                    DB.delete_tusapoint(tusapoint_id)
                    tusabot.send_message(last_chat_id, 'Стёр: '+ description_13 +'...')
        
                        
                elif last_chat_text == 'like_tusapoint':
                    author_likes_id = DB.get_friend(telegram_id=last_chat_id)['id']
                    heart = '♥'
                    if not DB.get_like(tusapoint_id,author_likes_id): #dict false if empty
                        DB.like(author_likes_id, tusapoint_id)                                           
                    else:
                        DB.delete_like(DB.get_like(tusapoint_id,author_likes_id)['id'])
                        heart = '🤍' 
                        
                        
                    keyboard = json.dumps({'inline_keyboard': [[
                            {'text': '🗑 del', 'callback_data': 'tusapoint delete_tusapoint '+str(tusapoint_id)},
                            {'text': heart , 'callback_data': 'tusapoint like_tusapoint '+str(tusapoint_id)}
                            ]]})
                    tusabot.edit_message(last_chat_id, last_message_id, DB.get_tusapoint(t_id = tusapoint_id)['description'] + '\n author: '+DB.get_friend(DB.get_tusapoint(t_id = tusapoint_id)['author_id'])['name'], keyboard)
        
        
                elif last_command.get(last_chat_id) == '/go_debts':
                    tusabot.send_message(last_chat_id, 'Вычисляю...')
                    try:                
                        users = {}
        #               format of input date(last text) (one string):
        #                 Чувак 1000\n
        #                 Чувиха 200\n
        #                 Парнишка 0\n
        #                 Девчонка 0
                        lst = last_chat_text.replace(' ', '\n').strip().split('\n')
                        print(lst)
                        for i in range(0,len(lst),2): users[lst[i]]= int(lst[i+1])
                        print(users)
                        trans = NOdebts.equally(users)
                        print(trans)
            
                        one_str = 'Вот список транзакций:\n'
                        for i in trans:
                            one_str += i+': '+ str(trans[i])+ '\n'
                        tusabot.send_message(last_chat_id, one_str)
                    except:
                        time.sleep(2)
                        tusabot.send_message(last_chat_id, 'Стоп. Что?')
                        tusabot.send_message(last_chat_id, 'Ты вообще не але? Я же сказал в каком виде должна быть информация')
                        
                    last_command[last_chat_id] = None
        
        
                elif last_command.get(last_chat_id) == '/new_tusapoint':
                    
                    if last_chat_text != None:
                        DB.add_tusapoint(last_chat_text, DB.get_friend(telegram_id=last_chat_id)['id'])
                        print(last_chat_text)
                        tusabot.send_message(last_chat_id, 'Записал')
                    else: 
                        tusabot.send_message(last_chat_id, 'Ну и как я должен это записать?? ')
                    
                    last_command[last_chat_id] = None
        
                elif last_chat_text.lower() == 'передай масло' or last_chat_text.lower() == 'чтобы передать масло':
                    tusabot.send_animation(last_chat_id, 'CgACAgQAAxkBAAIO_V-OnUVz4i4-6cTCBuGyEyxcspgmAAIyAgAC6ZTVUgTAwPe2YsA-GwQ')
                    tusabot.send_message(last_chat_id, 'OMG')
        
                else:
                    tusabot.send_message(last_chat_id, 'Что это?')
        
        
                offset = last_update_id + 1
            
        except:
            if offset != None: offset = offset + 1
#            print(DB.get_admin(1))
#            print(DB.get_friend(1))
            for admin in DB.get_admin():   
                tusabot.send_message(DB.get_friend(friend_id = admin['friends_id'])['telegram_id'], 'Произошла ошибка после этого сообщения:')
                tusabot.send_message(DB.get_friend(friend_id = admin['friends_id'])['telegram_id'], str(last_update))




if __name__ == '__main__':
#    for i in range(2):
#        try:
#            start_tusabot()
#        except:
#            print('except',i)
#            time.sleep(5*(1+i))
    start_tusabot()
    

