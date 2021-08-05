import telebot
from telebot import types
from Helper import *

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	output = """
Привет, я могу прислать тебе котенка.
Если хочешь - пиши /cat \n
Еще могу прислать курс криптовалюты в выбранной тобой валюте - пиши /info \n
	"""
	bot.send_message(message.from_user.id, 
		output, reply_markup=types.ReplyKeyboardRemove()
	)

@bot.message_handler(commands=['info'])
def info(message):
	bot.send_message(message.from_user.id, "Какая криптовалюта?")

def main(message):
	global crypto_currency, currency
	t = 2
	try:
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
		bot.send_message(message.from_user.id, output, reply_markup=types.ReplyKeyboardRemove())
	except:
		pass

@bot.message_handler(func=lambda message: True)
def send(message):

	global crypto_currency
	global currency

	if "/info" not in message.text:

		s = False

		for cur, name in get_currency_list():
			if message.text == cur + "-" + name:
				currency = message.text.split('-', 1)[0]
				main(message)
				s = True
				break

		if not s:
			try:
				crypto_currency = message.text
				for crypto in get_crypto_currency_list():
					if crypto.lower() == crypto_currency.lower():
						markup = types.ReplyKeyboardMarkup()
						for cur, name in get_currency_list():
							button = types.KeyboardButton(cur + "-" + name)
							markup.row(button)
						bot.send_message(message.from_user.id, "Выбери валюту:", reply_markup=markup)
						break
			except:
				pass

@bot.message_handler(commands=['cat'])
def send_cat(message):
	cat = open('cat.png', 'rb')
	bot.send_message(message.from_user.id, 
		"Нет, лучше посмотри что такое КУБИТ"
	)
	bot.send_photo(message.from_user.id, cat, reply_markup=types.ReplyKeyboardRemove())

bot.polling()