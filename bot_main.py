import os
import telebot
from currency_funcs_endpoint import get_fxmarket_currencies, exchange_currency, get_7_days_graph

API_KEY_TELEBOT = os.environ['API_KEY_TELEBOT'] #getenv('API_KEY')

print('API_KEY_TELEBOT: ', API_KEY_TELEBOT) ################## test

bot = telebot.TeleBot(API_KEY_TELEBOT)

@bot.message_handler(commands=['Hey'])
def hey(message):
    bot.reply_to(message, "hey? buba!!!")

@bot.message_handler(commands=['Say_hello_to_kozya'])
def hey(message):
    bot.send_message(message.chat.id, "kozya?? BUBUKA!!!) Yeeeaaaa!!")

@bot.message_handler(commands=['list'])
def currency_list(message):
    columns = get_fxmarket_currencies()
    bot.send_message(message.chat.id, columns)

'''
def check_message_exchange(message):
    exchange_message = message.text.split()
    print(exchange_message)
    if len(exchange_message)<2:
        return False
    else:
        return True'''

@bot.message_handler(commands=['exchange']) #,func=check_message_exchange)
def exchange_rate(message):
    exchanged = exchange_currency(message.text.split())
    bot.send_message(message.chat.id, 'exchange: {}'.format(exchanged))
    
@bot.message_handler(commands=['history'])
def history_7(message):
    result = get_7_days_graph(message.text.split()[1])
    bot.send_photo(message.chat.id, photo = open(result, 'rb'))

bot.polling()


