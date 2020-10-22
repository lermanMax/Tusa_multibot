import requests

class BotClass:

    def __init__(self, token, proxies=None):
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