import telebot
from Helper import CryptoCurrency, get_rate

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	output = """
Привет, я могу прислать тебе котенка.
Если хочешь - пиши /cat \n
Еще могу прислать курс криптовалюты в выбранной тобой валюте - пиши /info {криптовалюта} {валюта} \n
Пример: /info btc rub
	"""
	bot.send_message(message.from_user.id, 
		output
	)

@bot.message_handler(commands=['info'])
def info(message):
	t = 2
	if message != '/info':
		m = message.text.replace('/info ', '')
		crypto_currency = m[0] + m[1] + m[2]
		currency = m[4] + m[5] + m[6]
		data = get_rate(currency=currency, crypto_currency=crypto_currency)
		output = """
{crypto_currency} -> {currency} 
Цена покупки: {buy_price} 
Цена продажи: {sell_price} 
Цена последней сделки: {last_price} 
Объем торгов в {crypto_currency}: {vol_cur} 
Объем торгов в {currency}: {vol} 
Наибольшая цена: {high_price} 
Наименьшая цена: {low_price} 
Средняя цена: {avg_price} 
		""".format(crypto_currency=crypto_currency.upper(), currency=currency.upper(),
		buy_price=round(data.buy_price, t),
		sell_price=round(data.sell_price, t),
		last_price=round(data.last_price, t),
		vol=round(data.vol, t),
		vol_cur=round(data.vol_cur, t),
		high_price=round(data.high_price, t),
		low_price=round(data.low_price, t),
		avg_price=round(data.avg_price, t))
		bot.send_message(message.from_user.id, output)
	

@bot.message_handler(commands=['cat'])
def send_cat(message):
	cat = open('cat.png', 'rb')
	bot.send_message(message.from_user.id, 
		"Нет, лучше посмотри что такое КУБИТ"
	)
	bot.send_photo(message.from_user.id, cat)

bot.polling()