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

DB = DB_tusabot.DB_tusabot(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)


def new_tusapoint(message):
    tusabot.send_message(message['chat_id'] , 'Что у тебя?')
    
    return 'reply_new_tusapoint'

def reply_new_tusapoint(message):
    
    if message['text'] != None:
        DB.add_tusapoint(message['text'], DB.get_friend(telegram_id=last_chat_id)['id'])
        print(message['text'])
        tusabot.send_message(message['chat_id'], 'Записал')
    else: 
        tusabot.send_message(message['chat_id'], 'Ну и как я должен это записать?? ')
    
    return None

def go_debts(message):
    tusabot.send_message(
            message['chat_id'], 
            'Напиши, кто сколько потратил?\nНужна инфа в таком виде:')
    
    tusabot.send_message(
            message['chat_id'], 
            'Чувак 1000\nЧувиха 200\nПарнишка 0\nДевчонка 0')
    
    return 'reply_go_debts'

def reply_go_debts(message):
    tusabot.send_message(message['chat_id'], 'Вычисляю...')
    try:                
        users = {}
#       format of input date(last text) (one string):
#         Чувак 1000\n
#         Чувиха 200\n
#         Парнишка 0\n
#         Девчонка 0
        lst = message['text'].replace(' ', '\n').strip().split('\n')
        print(lst)
        for i in range(0,len(lst),2): users[lst[i]]= int(lst[i+1])
        print(users)
        trans = NOdebts.equally(users)
        print(trans)
    
        text = 'Вот список транзакций:\n'
        for i in trans:
            text += i+': '+ str(trans[i])+ '\n'
        tusabot.send_message(message['chat_id'], text)
    except:
        time.sleep(2)
        tusabot.send_message(message['chat_id'],
                             'Стоп. Что?')
        tusabot.send_message(message['chat_id'], 
        'Ты вообще не але? Я же сказал в каком виде должна быть информация')
    
    return None

def make_list_tusapoints(DB=DB):
    text = 'Вот список тусапоинтов:\n'
    tusapoints = DB.get_tusapoint()
    for row in tusapoints:
        text += ('◾' 
                    + row['description'] 
                    +' ♥'
                    + str(len(DB.get_like(row['id'])))
                    + '\n')
        
    keyboard = json.dumps({'inline_keyboard': [[
        {'text': '✏ edit', 
         'callback_data': '{"command": "edit_list_of_tusapoints" }' 
        },
        {'text': '🔄 update', 
         'callback_data': '{"command": "update_list_of_tusapoints" }' 
        },                  
        ]]})
    
    return text, keyboard
    

def get_list(message):
    text, keyboard = make_list_tusapoints()
    tusabot.send_message(message['chat_id'], one_str, keyboard)
    return None


def update_list_of_tusapoints(message):
    text, keyboard = make_list_tusapoints()
    tusabot.edit_message(message['chat_id'], 
                         message['message_id'], 
                         text, 
                         keyboard)
    return None


def make_text_keyboard_tusapoint(tusapoint, heart, DB=DB):
    del_data = {"command": "delete_tusapoint" , "id": tusapoint['id'] }
    heart_data = {"command": "like_tusapoint", "id": tusapoint['id'] }
                        
    keyboard = json.dumps({'inline_keyboard': [[
            {'text': '🗑 del', 
             'callback_data': str(del_data)
            },
            {'text': heart, 
             'callback_data': str(heart_data)
            }
            ]]})

    text = (tusapoint['description'] 
            + '\n' 
            + '🖋author: '
            + DB.get_friend(tusapoint['author_id'])['name']
            )
    
    return text, keyboard

def edit_list_of_tusapoints(message, DB=DB):
                    
    tusapoints = DB.get_tusapoint()
    for row in tusapoints:
        heart = '🤍'
        user_id = DB.get_friend(telegram_id = message['chat_id'])['id']        
        if DB.get_like(row['id'], user_id): heart = '♥'
        
        text, keyboard = make_text_keyboard_tusapoint(tusapoint=row, heart, DB=DB)
        
        
        tusabot.send_message(message['chat_id'], text, keyboard)
    
    return None

def delete_tusapoint(message):
    tusapoint_id = message['data']['id']
    description_13 = DB.get_tusapoint(t_id = tusapoint_id)['description'][0:13]
    DB.delete_tusapoint(tusapoint_id)
    tusabot.send_message(last_chat_id, 'Стёр: '+ description_13 + '...')
    return None


def like_tusapoint(message):
    tusapoint_id = message['data']['id']
    author_likes_id = DB.get_friend(telegram_id=message['chat_id'])['id']
    heart = '♥'
    if not DB.get_like(tusapoint_id,author_likes_id): #dict false if empty
        DB.like(author_likes_id, tusapoint_id)                                           
    else:
        DB.delete_like(DB.get_like(tusapoint_id,author_likes_id)['id'])
        heart = '🤍' 
    
    tusapoint = DB.get_tusapoint(t_id = tusapoint_id)    
        
    text, keyboard = make_text_keyboard_tusapoint(tusapoint, heart, DB=DB)
    
    tusabot.edit_message(message['chat_id'], 
                         message['message_id'], 
                         text, 
                         keyboard)
    
    return None



def wtf_respons(message):
    
    if 'text' in message:
        if message['text'].lower() in ('передай масло','чтобы передать масло'):
            tusabot.send_animation(message['chat_id'], 
               'CgACAgQAAxkBAAIO_V-OnUVz4i4-6cTCBuGyEyxcspgmAAIyAgAC6ZTVUgTAwPe2YsA-GwQ')
            tusabot.send_message(message['chat_id'], 'OMG')
        
        else: tusabot.send_message(message['chat_id'], 'Что это?')
        
    else: tusabot.send_message(message['chat_id'], 'Что это?') 
  
  


do_command = {
        
        '/new_tusapoint': new_tusapoint,
        'reply_new_tusapoint': reply_new_tusapoint, 
        
        '/go_debts': go_debts,
        'reply_go_debts': reply_go_debts,
        
        '/get_list': get_list,
        'update_list_of_tusapoints': update_list_of_tusapoints,
        'edit_list_of_tusapoints': edit_list_of_tusapoints,
        
        'delete_tusapoint': delete_tusapoint,
        'like_tusapoint': like_tusapoint,
        
        
        }


@click.command()
@click.argument('proxies_on')
def start_tusabot(proxies_on = 'no'):
    proxies = None
    if proxies_on =='yes': proxies = socks
    
    tusabot = MyTelegramBotLib.BotClass(token,proxies)

    today = datetime.datetime.now().day
    
    expected_command = {} # key = chat id, value = last user's command 
    how_saw_hello = set()
    
    offset = None
    last_update = None
    
    
    while True:
        try:
    # ------------------------------------------------------------------------------
    # этот блок получает обновления от бота
            
            list_messages = tusabot.get_list_messages(offset)

            if not list_messages: continue
        
    
            for message in list_messages: 
                
                if message['type'] == 'callback_query':
                    message['is_command'] = True
                    message['data'] = json.loads(message['data'])
                    message['command'] = message['data']['command']
                    
                elif message['type'] == 'message':
                    if message['text'] in do_command:
                        message['is_command'] = True
                        message['command'] = message['text']
                    
                    else: message['is_command'] = False

                else: message['is_command'] = False
  
    # ------------------------------------------------------------------------------
    # логика бота                      
            
            for message in list_messages:
                
                last_update_id = message['update_id']
                
                if message['is_command']:
                    resp = do_command[message['command']](message)
                    expected_command[message['chat_id']] = resp
                
                else:
                    command = expected_command.get(message['chat_id']) 
                    if command:
                        resp = do_command[command](message)
                        expected_command[message['chat_id']] = resp
                    else:
                        wtf_respons(message)
            
            offset = last_update_id + 1
                        

            
#                if today == datetime.datetime.now().day and 5 <= datetime.datetime.now().hour < 6:
#                    how_saw_hello.clear()
#                    today += 1
#        
#                if last_chat_id not in how_saw_hello:
#                    tusabot.send_message(last_chat_id, 
#                                         'Приветствую, {}. Для чего я создан?'.format(last_chat_name))
#                    how_saw_hello.add(last_chat_id)


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
    

