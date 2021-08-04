import requests
import xmltodict

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
        if cur['CharCode'].lower() == currency:
            s = cur['Value']
            s = s.replace(',', '.')
            value = float(s)
    if currency == 'usd':
        value /= usd_rub
    else:
        value *= usd_rub
    obj = get_rate_usd(crypto_currency)
    obj.high_price *= value
    obj.low_price *= value
    obj.avg_price *= value
    obj.vol *= value
    obj.last_price *= value
    obj.buy_price *= value
    obj.sell_price *= value
    return obj

# def buy(crypto_currency: str) -> bool:
