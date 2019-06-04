import telebot
import random

token = '864588130:AAEGaWNYx18GFvMO4BLc0_9MCmXK9HQ01n8'
bot = telebot.TeleBot(token)

greetings = ['хола', 'хэллоу', 'здравствуй', 'привет', 'хай', 'здравствуй', 'приветствую', 'hi', 'hello']
invokers = greetings[:]
invokers.append('bot01')


@bot.message_handler(func=lambda message: True)
def say_hi(message):
    if message.text.lower() in invokers:
        bot.reply_to(message, random.choice(greetings).capitalize() + ', ' + message.from_user.username + '!')


bot.polling()
