import requests
import psycopg2
import time
import datetime
import matplotlib.pyplot
import sys
import os

api_key_fx = os.environ['API_KEY_FXMARKET']

def exchange_currency(exchange_message):
    #(quantity=10, currency1 = 'USD', currency2='CAD')

    print(exchange_message, len(exchange_message))
    
    if len(exchange_message) == 5 and exchange_message[1].isnumeric() and exchange_message[2].isalpha() and exchange_message[4].isalpha():

        #available_currencies_dict_saved_response =  {'currencies': {'USDAED': 'United Arab Emirates Dirham', 'USDARS': 'Argentine Peso', 'USDAUD': 'Australian Dollar', 'USDBRL': 'Brazilian Real', 'USDBTC': 'Bitcoin', 'USDCAD': 'Canadian Dollar', 'USDCHF': 'Swiss Franc', 'USDCLP': 'Chilean Peso', 'USDCNY': 'Chinese Yuan', 'USDCOP': 'Colombian Peso', 'USDCZK': 'Czech Koruna', 'USDDKK': 'Danish Krone', 'USDEUR': 'Euro', 'USDGBP': 'British Pound Sterling', 'USDHKD': 'Hong Kong Dollar', 'USDHUF': 'Hungarian Forint', 'USDHRK': 'Croatian Kuna', 'USDIDR': 'Indonesian Rupiah', 'USDILS': 'Israeli Sheqel', 'USDINR': 'Indian Rupee', 'USDISK': 'Icelandic Krona', 'USDJPY': 'Japanese Yen', 'USDKRW': 'South Korean Won', 'USDKWD': 'Kuwaiti Dinar', 'USDMXN': 'Mexican Peso', 'USDMYR': 'Malaysian Ringgit', 'USDMAD': 'Moroccan Dirham', 'USDNOK': 'Norwegian Krone', 'USDNZD': 'New Zealand Dollar', 'USDPEN': 'Peruvian Nuevo Sol', 'USDPHP': 'Philippine Peso', 'USDPLN': 'Polish Zloty', 'USDRON': 'Romanian Leu', 'USDRUB': 'Russian Ruble', 'USDSEK': 'Swedish Krona', 'USDSGD': 'Singapore Dollar', 'USDTHB': 'Thai Baht', 'USDTRY': 'Turkish Lira', 'USDTWD': 'Taiwanese Dollar', 'USDXAG': 'Silver (ounce)', 'USDXAU': 'Gold (ounce)', 'USDZAR': 'South African Rand'}}
        
        exchange_response = requests.get('https://fxmarketapi.com/apilive?api_key={}&currency={}'.format(api_key_fx, exchange_message[2]+exchange_message[4]))
        print(exchange_response)
        exchange_dict = exchange_response.json()
        print(exchange_dict)
        
        exchanged = exchange_message[4] + ' ' + "{:.2f}".format(float(exchange_message[1])*exchange_dict['price'][exchange_message[2]+exchange_message[4]])
        
        print(exchange_dict, exchanged)
    
    return exchanged


###############################


def get_fxmarket_currencies():
    conn = psycopg2.connect("dbname=exchange_bot_db user=postgres password=postgres")
    #cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cur = conn.cursor()


    #api_key = 'qKSMdVTy4MiefHpatSaB'

    available_currencies = 'https://fxmarketapi.com/apicurrencies'

    #querystring_av = {"api_key":api_key_fx}

    get_currencies = str()
    
    ### fiest request: to get dict of available currencies for exchange
    available_currencies_dict_response = requests.get(available_currencies, params={"api_key":api_key_fx})
    #available_currencies_dict_response =  {'currencies': {'USDAED': 'United Arab Emirates Dirham', 'USDARS': 'Argentine Peso', 'USDAUD': 'Australian Dollar', 'USDBRL': 'Brazilian Real', 'USDBTC': 'Bitcoin', 'USDCAD': 'Canadian Dollar', 'USDCHF': 'Swiss Franc', 'USDCLP': 'Chilean Peso', 'USDCNY': 'Chinese Yuan', 'USDCOP': 'Colombian Peso', 'USDCZK': 'Czech Koruna', 'USDDKK': 'Danish Krone', 'USDEUR': 'Euro', 'USDGBP': 'British Pound Sterling', 'USDHKD': 'Hong Kong Dollar', 'USDHUF': 'Hungarian Forint', 'USDHRK': 'Croatian Kuna', 'USDIDR': 'Indonesian Rupiah', 'USDILS': 'Israeli Sheqel', 'USDINR': 'Indian Rupee', 'USDISK': 'Icelandic Krona', 'USDJPY': 'Japanese Yen', 'USDKRW': 'South Korean Won', 'USDKWD': 'Kuwaiti Dinar', 'USDMXN': 'Mexican Peso', 'USDMYR': 'Malaysian Ringgit', 'USDMAD': 'Moroccan Dirham', 'USDNOK': 'Norwegian Krone', 'USDNZD': 'New Zealand Dollar', 'USDPEN': 'Peruvian Nuevo Sol', 'USDPHP': 'Philippine Peso', 'USDPLN': 'Polish Zloty', 'USDRON': 'Romanian Leu', 'USDRUB': 'Russian Ruble', 'USDSEK': 'Swedish Krona', 'USDSGD': 'Singapore Dollar', 'USDTHB': 'Thai Baht', 'USDTRY': 'Turkish Lira', 'USDTWD': 'Taiwanese Dollar', 'USDXAG': 'Silver (ounce)', 'USDXAU': 'Gold (ounce)', 'USDZAR': 'South African Rand'}}

    for i in available_currencies_dict_response.json()['currencies']:
        get_currencies += i
        get_currencies += ','

    currencies = get_currencies[:-1]
    #print(currencies)
    
    #### second request: to get dict with actual exchange rates. In current case: USD  to all another currencies
    exchange_rates_url = 'https://fxmarketapi.com/apilive?api_key={}&currency={}'.format(api_key_fx, currencies)
    #response1 = {'price': {'USDAED': 3.67341, 'USDARS': 97.69935, 'USDAUD': 1.35768, 'USDBRL': 5.18603, 'USDBTC': 2e-05, 'USDCAD': 1.26199, 'USDCHF': 0.91546, 'USDCLP': 771.22518, 'USDCNY': 6.45971, 'USDCOP': 3759.5864, 'USDCZK': 21.888, 'USDDKK': 6.2805, 'USDEUR': 0.8446, 'USDGBP': 0.72613, 'USDHKD': 7.77724, 'USDHRK': 6.3263, 'USDHUF': 293.87799, 'USDIDR': 14239.86621, 'USDILS': 3.2069, 'USDINR': 72.99308, 'USDISK': 126.69412, 'USDJPY': 110.0295, 'USDKRW': 1156.21837, 'USDKWD': 0.30063, 'USDMAD': 8.94742, 'USDMXN': 19.99324, 'USDMYR': 4.15334, 'USDNOK': 8.69509, 'USDNZD': 1.41443, 'USDPEN': 4.09089, 'USDPHP': 49.92553, 'USDPLN': 3.8062, 'USDRON': 4.16848, 'USDRUB': 72.98147, 'USDSEK': 8.60906, 'USDSGD': 1.34463, 'USDTHB': 32.3155, 'USDTRY': 8.29781, 'USDTWD': 27.73255, 'USDXAG': 0.04142, 'USDXAU': 0.00055, 'USDZAR': 14.40648}, 'timestamp': 1630531330}
    exchange_rates_response = requests.get(exchange_rates_url)

    exchange_rates_dict = exchange_rates_response.json()
    print('execute: ', cur.execute("SELECT * FROM currency_exchange_rates;"))
    check_time = cur.fetchone()
    print('fetchone: ', cur.fetchone(), check_time[2], exchange_rates_dict['timestamp'])
    
    columns = str()
    
    ### checking if user made request again less then 10 min after previous request to deside where to get info:
    ### if less then 10 min - from db, if more - from new request to the exchange website
    if check_time[2] + 600 < exchange_rates_dict['timestamp']:
        #print(exchange_rates_dict['timestamp'], type(exchange_rates_dict['timestamp']))
        for i in exchange_rates_dict['price']:
            columns += i[3:]
            columns += ' : '
            columns += "{:.2f}".format(exchange_rates_dict['price'][i])
            columns += '\n'
            #cur.execute('INSERT INTO currency_exchange_rates (currency, value, timestamp) VALUES (%s, %s, %s);', (i[3:], "{:.2f}".format(exchange_rates_dict['price'][i]), exchange_rates_dict['timestamp']))
            cur.execute('UPDATE currency_exchange_rates SET value = %s, timestamp = %s WHERE currency = %s;', ("{:.2f}".format(exchange_rates_dict['price'][i]), exchange_rates_dict['timestamp'], i[3:]))
            conn.commit()
            #### there is an ISSUE with two decimal precision - GOLD is too expansive for USD and we get value 0,0004. And with two decimal precision we get 0,00.

        print('columns string: ', columns, '\n')

        print('10 min passed: cur execute: ', cur.execute("SELECT * FROM currency_exchange_rates;", '\n'))

        print('10 min passed: fetchall: ', cur.fetchall())
    
    else:
        print('wait 10 min: cur execute: ', cur.execute("SELECT currency, value FROM currency_exchange_rates;", '\n'))
        raw_columns = cur.fetchall()
        print('wait 10 min: fetchall: ', raw_columns)
        
        for i in raw_columns:
            columns += i[0]
            columns += ' : '
            columns += str(i[1])
            columns += '\n'
        
    print(columns)
    cur.close()
    conn.close()
    
    return columns


###############################


def get_7_days_graph(currency):
    print('INPUT = ', currency)
    today = datetime.datetime.fromtimestamp(int(time.time()))
    week_ago = datetime.datetime.fromtimestamp(int(time.time())-604800)
    #currency = 'EURRUB'
    matplotlib.use('Agg')

    exchange_response = requests.get('https://fxmarketapi.com/apitimeseries?currency={}&start_date={}&end_date={}&interval=daily&api_key={}'.format(currency, str(week_ago).split()[0], str(today).split()[0], api_key_fx))

    #exchange_response = {'end_date': '2021-09-03-10:00', 'price': { '2021-08-26': {'EURUSD': {'close': 1.1752, 'high': 1.1779, 'low': 1.1746, 'open': 1.17722}, 'GBPUSD': {'close': 1.37001, 'high': 1.37681, 'low': 1.36896, 'open': 1.3761}}, '2021-08-27': {'EURUSD': {'close': 1.17945, 'high': 1.18023, 'low': 1.1735, 'open': 1.17517}, 'GBPUSD': {'close': 1.37633, 'high': 1.37815, 'low': 1.36801, 'open': 1.36976}}, '2021-08-30': {'EURUSD': {'close': 1.17967, 'high': 1.18098, 'low': 1.17827, 'open': 1.17954}, 'GBPUSD': {'close': 1.37593, 'high': 1.37754, 'low': 1.37336, 'open': 1.37613}}, '2021-08-31': {'EURUSD': {'close': 1.18085, 'high': 1.1845, 'low': 1.17945, 'open': 1.17967}, 'GBPUSD': {'close': 1.3749, 'high': 1.38081, 'low': 1.37428, 'open': 1.37668}}, '2021-09-01': {'EURUSD': {'close': 1.18403, 'high': 1.18572, 'low': 1.17935, 'open': 1.18097}, 'GBPUSD': {'close': 1.37692, 'high': 1.37984, 'low': 1.37313, 'open': 1.37541}}, '2021-09-02': {'EURUSD': {'close': 1.18394, 'high': 1.18459, 'low': 1.18373, 'open': 1.1842}, 'GBPUSD': {'close': 1.37764, 'high': 1.37799, 'low': 1.37678, 'open': 1.37756}}}, 'start_date': '2021-07-02-00:00'}

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
        print(date, exchange_response.json()['price'][date][currency]['close'], '\n')

    print(fx_date, '\n', fx_close, '\n',fx_high  , '\n',fx_low, '\n',fx_open)
     
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
    
    #matplotlib.pyplot.show()
    matplotlib.pyplot.close()
    return image_name


if __name__ == "__main__":
    exchange_currency(['/exchange', '10', 'USD', 'to', 'CAD'])
    get_7_days_graph('EURRUB')
