# -*- coding: utf-8 -*-

'''
Бот для Telegram

Version: 0.1.0
- Программа реализована на ООП
'''

import requests
import datetime

class NoUpdatesException(Exception):
	
	def __init__(self, length, atleast):
		Exception.__init__(self)
		self.length = length
		self.atleast = atleast

class Bot01:

	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)

	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		response = requests.get(self.api_url + method, params)
		result_json = response.json()['result']
		return result_json

	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		method = 'sendMessage'
		response = requests.post(self.api_url + method, params)
		return response

	def get_last_update(self):
		get_result = self.get_updates()
		print(len(get_result))

		if len(get_result) > 0:
			last_update = get_result[-1]
		elif len(get_result) == 0:
			raise NoUpdatesException(len(get_result), 1)
		else:
			last_update = get_result[len(get_result)-1]

		return last_update

	def get_updates_json(request):
		params = {'timeout': 100, 'offset': None}
		response = requests.get(request + 'getUpdates', data=params)
		return response.json()

### Main Function ###

token = '864588130:AAEGaWNYx18GFvMO4BLc0_9MCmXK9HQ01n8'
greet_bot = Bot01(token)
greetings = ('хола', 'хэллоу', 'здравствуй', 'привет', 'хай', 'bot01')
now = datetime.datetime.now()

def main():
	new_offset = None
	today = now.day
	hour = now.hour

	while True:
		greet_bot.get_updates(new_offset)

		try:
			last_update = greet_bot.get_last_update()
		except NoUpdatesException as no:
			continue

		last_update_id = last_update['update_id']
		last_chat_text = last_update['message']['text']
		last_chat_id = last_update['message']['chat']['id']
		last_chat_name = last_update['message']['from']['first_name']

		if last_chat_text.lower() in greetings and today == now.day and 6 <= hour <= 12:
			greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
			today += 1

		elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour <= 17:
			greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))

		elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
			greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))

		new_offset = last_update_id + 1

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()