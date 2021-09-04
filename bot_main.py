import os
import telebot
from currency_funcs_endpoint import get_fxmarket_currencies, exchange_currency, get_7_days_graph
from bot_server_db import server
from flask import Flask, request


API_KEY_TELEBOT = os.environ['API_KEY_TELEBOT']

bot = telebot.TeleBot(API_KEY_TELEBOT)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, 'Weclome to currency exchange bot. Available commands are /list, /exchange and /history.')
    except:
        bot.reply_to(message, 'Something went wrong.')

@bot.message_handler(commands=['help'])
def hlep(message):
    try:
        bot.send_message(message.chat.id, 'Here should be some hLep and explanations for functions. But you already know the stuff...')
    except:
        bot.reply_to(message, 'Wrong hLep.')


@bot.message_handler(commands=['list'])
def currency_list(message):
    try:
        columns = get_fxmarket_currencies()
        bot.send_message(message.chat.id, columns)
    except:
        bot.reply_to(message, 'Use this message format: "/list". No additional arguments are required.')
        ### you can write everything after "/list"... Does it matter???

@bot.message_handler(commands=['exchange']) 
def exchange_rate(message):
    try:
        exchanged = exchange_currency(message.text.split())
        bot.send_message(message.chat.id, 'exchange: {}'.format(exchanged))
    except:
        bot.reply_to(message, 'Use this message format: "/exchange 100 USD to EUR". Where "100" - amount requested for exchange, "USD" - currency to sold, "EUR" - currency to buy. Also you may check if your currency is in exchange list using command "/list"')
        ### instead of word "to" you can insert anything... Does it matter???

@bot.message_handler(commands=['history'])
def history_7(message):
    try:
        result = get_7_days_graph(message.text.split()[1])
        bot.send_photo(message.chat.id, photo = open(result, 'rb'))
    except:
        bot.reply_to(message, 'Use this message format: "/history USDEUR". Where "USDEUR" consist of two currencies (USD and EUR for example): first - currency for which prices would be placed on graphs (to buy), second - currency value of which is set to 1 (to sold).') 

@server.route('/' + API_KEY_TELEBOT, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://teleg1exchange1bot.herokuapp.com/' + API_KEY_TELEBOT)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #bot.polling() ### no need for polling when use webhook #bot.polling()
