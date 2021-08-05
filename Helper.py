import requests
import xmltodict
import os
import json
import urllib, http.client
import hmac, hashlib

class CryptoCurrency:

    def __init__(self, 
                 high_price,
                 low_price,
                 avg_price,
                 vol,
                 vol_cur,
                 last_price,
                 buy_price,
                 sell_price,
                 char_code
        ):
        self.high_price = high_price
        self.low_price = low_price
        self.avg_price = avg_price
        self.vol = vol
        self.vol_cur = vol_cur
        self.last_price = last_price
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.char_code = char_code

def get_rate_usd(crypto_currency: str) -> CryptoCurrency:
    response = requests.get(
        'https://yobit.net/api/3/ticker/' + 
        crypto_currency + '_usd'
    ).json()[crypto_currency + '_usd']
    return CryptoCurrency(
        high_price = response['high'],
        low_price = response['low'],
        avg_price = response['avg'],
        vol = response['vol'],
        vol_cur = response['vol_cur'],
        last_price = response['last'],
        buy_price = response['buy'],
        sell_price = response['sell'],
        char_code = crypto_currency
    )

def get_currency_list():
    res = []
    response = requests.get('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    data = dict(xmltodict.parse(response.content)['ValCurs'])['Valute']
    for cur in data:
        res.append((cur['CharCode'], cur['Name']))
    return res

def get_crypto_currency_list():
    res = []
    response = requests.get(
        'https://yobit.net/api/3/info/'
    ).json()['pairs']
    for pair in response:
        crypto_currency = pair.split('_', 1)[0]
        res.append(crypto_currency.upper())
    return list(set(res))

def get_rate(currency: str, crypto_currency: str) -> CryptoCurrency:
    response = requests.get('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    data = dict(xmltodict.parse(response.content)['ValCurs'])['Valute']
    value = 1
    usd_rub = 0
    for cur in data:
        if cur['CharCode'].lower() == 'usd':
            s = cur['Value']
            s = s.replace(',', '.')
            usd_rub = float(s)
    for cur in data:
        if cur['CharCode'].lower() == currency.lower():
            s = cur['Value']
            s = s.replace(',', '.')
            value = float(s)
    if currency.lower() == 'usd':
        value /= usd_rub
    else:
        value *= usd_rub
    obj = get_rate_usd(crypto_currency.lower())
    obj.high_price *= value
    obj.low_price *= value
    obj.avg_price *= value
    obj.vol *= value
    obj.last_price *= value
    obj.buy_price *= value
    obj.sell_price *= value
    return obj

def trade_buy(crypto_currency: str, amount=0, rate=0):

    if rate == 0:
        # rate = get_rate(btc, usd)
        pass

    response = call_api(method='Trade', pair=crypto_currency + '_btc', type='buy', rate=rate, amount=amount)

    if response['success'] == '1':
        try:
            return True, response['received'], response['remains'], response['funds'], response['order_id']
        except KeyError:
            return False, 0, 0, 0, 0
    return False, 0, 0, 0, 0

def trade_sell(crypto_currency: str, amount=0, rate=0):

    if rate == 0:
        # rate = get_rate(btc, usd)
        pass

    response = call_api(method='Trade', pair=crypto_currency + '_btc', type='sell', rate=rate, amount=amount)
    
    if response['success'] == '1':
        try:
            return True, response['received'], response['remains'], response['funds'], response['order_id']
        except KeyError:
            return False, 0, 0, 0, 0
    return False, 0, 0, 0, 0

def call_api(**kwargs):
    with open('nonce', 'r+') as inp:
        nonce = int(inp.read())
        inp.seek(0)
        inp.write(str(nonce+1))
        inp.truncate()
    payload = {'nonce': nonce}
    if kwargs:
        payload.update(kwargs)
    
    API_KEY = '7F9D650D1944A7DA183C09BF06713DC7'
    API_SECRET = b'e41437a1818fe37962fb282ee82f437b'

    payload =  urllib.parse.urlencode(payload)

    H = hmac.new(key=API_SECRET, digestmod=hashlib.sha512)
    H.update(payload.encode('utf-8'))
    sign = H.hexdigest()

    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Key":API_KEY,
            "Sign":sign}
    conn = http.client.HTTPSConnection("yobit.net", timeout=60)
    conn.request("POST", "/tapi/", payload, headers)
    response = conn.getresponse().read()

    conn.close()

    obj = json.loads(response.decode('utf-8'))

    return obj

def balance():
    response = call_api(method='getInfo')

    funds, funds_incl_orders = 0,  0

    try:
        funds = response['return']['funds']
        funds_incl_orders = response['return']['funds_incl_orders']
    except:
        pass

    if response['success'] == 1:
        try:
            return True, funds, funds_incl_orders, response['return']['transaction_count'], response['return']['open_orders']
        except KeyError:
            return False, 0, 0, 0, 0
    return False, 0, 0, 0, 0

