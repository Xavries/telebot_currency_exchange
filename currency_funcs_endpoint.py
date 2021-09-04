import requests
import time
import datetime
import matplotlib.pyplot
import sys
import os
from bot_server_db import db, Bot_ex


api_key_fx = os.environ['API_KEY_FXMARKET']

db.session.add(Bot_ex(currency = 'USD', value = 1.00, timestamp = 1630608806))
db.session.commit()

def exchange_currency(exchange_message):

    ### DEV print(exchange_message, len(exchange_message))
    
    if len(exchange_message) == 5 and exchange_message[1].isnumeric() and exchange_message[2].isalpha() and exchange_message[4].isalpha():

        exchange_response = requests.get('https://fxmarketapi.com/apilive?api_key={}&currency={}'.format(api_key_fx, exchange_message[2]+exchange_message[4]))
        ### DEV print(exchange_response)
        exchange_dict = exchange_response.json()
        ### DEV print(exchange_dict)
        
        exchanged = exchange_message[4] + ' ' + "{:.2f}".format(float(exchange_message[1])*exchange_dict['price'][exchange_message[2]+exchange_message[4]])
        
        ### DEV print(exchange_dict, exchanged)
    
    return exchanged


###############################


def get_fxmarket_currencies():

    available_currencies = 'https://fxmarketapi.com/apicurrencies'

    get_currencies = str()
    
    ### first request: to get dict of available currencies for exchange
    available_currencies_response = requests.get(available_currencies, params={"api_key":api_key_fx})
    available_currencies_dict = available_currencies_response.json()
    ### DEV print(available_currencies_dict)
    available_currencies_dict['currencies'].pop('BTCUSD')
    available_currencies_dict['currencies']['USDBTC'] = 'Bitcoin'
    ### DEV print(available_currencies_dict)
    for i in available_currencies_dict['currencies']:
        get_currencies += i
        get_currencies += ','

    currencies = get_currencies[:-1]
    ### DEV print(currencies)
    
    #### second request: to get dict with actual exchange rates. In current case: USD  to all another currencies
    exchange_rates_url = 'https://fxmarketapi.com/apilive?api_key={}&currency={}'.format(api_key_fx, currencies)
    exchange_rates_response = requests.get(exchange_rates_url)

    exchange_rates_dict = exchange_rates_response.json()
    ### DEV print(exchange_rates_dict['price'])
    ### DEV print('execute: ', db.session.query(Bot_ex).all())
    check_time = Bot_ex.query.first()        
    ### DEV print('check_time: ', check_time, check_time.timestamp, exchange_rates_dict['timestamp'])
    
    columns = 'USD : 1.00\n'
    
    ### checking if user made request again less then 10 min after previous request to deside where to get info:
    ### if less then 10 min - from db, if more - from new request to the exchange website
    if check_time.timestamp + 600 < exchange_rates_dict['timestamp']:
        Bot_ex.query.delete()
        db.session.commit()
        for i in exchange_rates_dict['price']:
            columns += i[3:]
            columns += ' : '
            columns += "{:.2f}".format(exchange_rates_dict['price'][i])
            columns += '\n'
            currency_rate = Bot_ex(currency = i[3:], value = "{:.2f}".format(exchange_rates_dict['price'][i]), timestamp = exchange_rates_dict['timestamp'])
            db.session.add(currency_rate)
            db.session.commit()
            #### there is an ISSUE with two decimal precision - XAU (gold) and BTC (bitcoin) are too expansive for USD and we get value 0,00055 and 2e-05. And with two decimal precision we get 0,00.

        ### DEV print('columns string: ', columns, '\n')

        ### DEV print('10 min passed: cur execute: ', Bot_ex.query.all())


    
    else:
        raw_columns = Bot_ex.query.all()
        ### DEV print('wait 10 min: query all: ', raw_columns)
        
        for i in raw_columns:
            columns += i.currency
            columns += ' : '
            columns += str(i.value)
            columns += '\n'
        
    ### DEV print(columns)
    
    return columns


###############################


def get_7_days_graph(currency):
    ### DEV print('INPUT = ', currency)
    today = datetime.datetime.fromtimestamp(int(time.time()))
    week_ago = datetime.datetime.fromtimestamp(int(time.time())-604800)
    
    matplotlib.use('Agg') ### we don't need GUI (Tkinter by default). It messes things up. It doesn't work at all or does not make new env and mixes all graphs into one.

    exchange_response = requests.get('https://fxmarketapi.com/apitimeseries?currency={}&start_date={}&end_date={}&interval=daily&api_key={}'.format(currency, str(week_ago).split()[0], str(today).split()[0], api_key_fx))
    ### DEV print(exchange_response.json())
    ### in case today is Saturday
    if 'weekend' in str(exchange_response.json()):
        today = datetime.datetime.fromtimestamp(int(time.time())-86400)
        week_ago = datetime.datetime.fromtimestamp(int(time.time())-604800-86400)
        
        exchange_response = requests.get('https://fxmarketapi.com/apitimeseries?currency={}&start_date={}&end_date={}&interval=daily&api_key={}'.format(currency, str(week_ago).split()[0], str(today).split()[0], api_key_fx))
        ### in case today is Sunday
        if 'weekend' in str(exchange_response.json()):
            today = datetime.datetime.fromtimestamp(int(time.time())-86400*2)
            week_ago = datetime.datetime.fromtimestamp(int(time.time())-604800-86400*2)
            
            exchange_response = requests.get('https://fxmarketapi.com/apitimeseries?currency={}&start_date={}&end_date={}&interval=daily&api_key={}'.format(currency, str(week_ago).split()[0], str(today).split()[0], api_key_fx))

    fx_date = list()
    fx_close = list()
    fx_high = list()
    fx_low = list()
    fx_open = list()

    for date in exchange_response.json()['price']:
        fx_date.append(str(date))
        fx_close.append(exchange_response.json()['price'][date][currency]['close'])
        fx_high.append(exchange_response.json()['price'][date][currency]['high'])
        fx_low.append(exchange_response.json()['price'][date][currency]['low'])
        fx_open.append(exchange_response.json()['price'][date][currency]['open'])
        ### DEV print(date, exchange_response.json()['price'][date][currency]['close'], '\n')

    ### DEV print(fx_date, '\n', fx_close, '\n',fx_high  , '\n',fx_low, '\n',fx_open)
     
    matplotlib.pyplot.plot(fx_date, fx_close, marker='o', label = "close")
    matplotlib.pyplot.plot(fx_date, fx_high, marker='o', label = "high")
    matplotlib.pyplot.plot(fx_date, fx_low, marker='o', label = "low")
    matplotlib.pyplot.plot(fx_date, fx_open, marker='o', label = "open")
     
    matplotlib.pyplot.xlabel('date')
    matplotlib.pyplot.ylabel('price')
     
    matplotlib.pyplot.title('7 days exchange rate')

    matplotlib.pyplot.legend()
    
    image_name = currency + '_graph_'+ fx_date[0] + fx_date[-1] + '.png'
    matplotlib.pyplot.savefig(image_name)
    
    #matplotlib.pyplot.show() ### DEV
    matplotlib.pyplot.close()
    return image_name


if __name__ == "__main__":
    exchange_currency(['/exchange', '10', 'USD', 'to', 'CAD'])
    get_7_days_graph('EURRUB')
