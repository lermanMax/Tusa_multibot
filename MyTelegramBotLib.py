import requests

class BotClass:

    def __init__(self, token=None, proxies=None):
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
    
    def edit_message(self, chat_id, message_id, text, reply_markup=None):
        method = 'editMessageText'
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'reply_markup': reply_markup}
        resp = requests.post(self.api_url + method, params, proxies = self.proxies)
        return resp
    
    def send_animation(self, chat_id, file_id, reply_markup=None):
        method = 'sendAnimation'
        params = {'chat_id': chat_id, 'animation': file_id, 'reply_markup': reply_markup}
        resp = requests.post(self.api_url + method, params, proxies = self.proxies)
        return resp

    def get_last_update(self, offset=None, timeout=100):
        get_result = self.get_updates(offset, timeout)

        if len(get_result) > 0: last_update = get_result[-1]
        else: last_update = None

        return last_update
    
    def get_list_messages(self, offset=None, timeout=100):
        get_result = self.get_updates(offset, timeout)
        
        list_messages = []
        '''
        [
        {
            'update_id': 00000000,
            'type': 'message',
            'chat_id': 00000000,
            'chat_name': 'Name',
            'text': 'some text'
        },
        {
            'update_id': 00000000,
            'type': 'callback_query'
            'chat_id': 00000000
            'chat_name': 'Name'
            'message_id': 00000000
            'data': '{"command":"name", "arg_1": 00 }'
        }, ...]
        '''
        for update in get_result:
            
            if update == None: continue
        
            message = {}
            message['update_id'] = update['update_id']
            
            if 'message' in update:
                message['type'] = 'message'
                message['chat_id'] = update['message']['from']['id']
                message['chat_name'] = update['message']['from']['first_name']
                message['text'] = update['message'].get('text')
    
            elif 'callback_query' in update:
                message['type'] = 'callback_query'
                message['chat_id'] = update['callback_query']['from']['id']
                message['chat_name'] = update['callback_query']['from']['first_name']
                message['message_id'] = update['callback_query']['message']['message_id']
                message['data'] = update['callback_query']['data']
            else:
                message['type'] = "unknown"
    
            list_messages.append(message)
            
        return list_messages

    