import telebot
from telebot import types
from Helper import *

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

current = ''

bot = telebot.TeleBot(API_TOKEN)

buy_a = None

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
	global current
	current = 'info'
	bot.send_message(message.from_user.id, "Какая криптовалюта?")

def send_info(message):
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

@bot.message_handler(commands=['buy'])
def buy(message):
	global current
	current = 'buy'
	bot.send_message(message.from_user.id, "Какая криптовалюта?")

@bot.message_handler(commands=['cat'])
def send_cat(message):
	global current
	print(message.from_user.id)
	current = 'cat'
	cat = open('cat.png', 'rb')
	bot.send_message(message.from_user.id, 
		"Нет, лучше посмотри что такое КУБИТ"
	)
	bot.send_photo(message.from_user.id, cat, reply_markup=types.ReplyKeyboardRemove())

def transaction(message):

	global crypto_currency
	global currency
	global buy_a
	global sell_a
	global rate

	if buy_a is not None:
		num = float(message.text)
		success = False
		received = 0
		remains = 0
		funds = 0
		if buy_a:
			success, received, remains, funds, order_id = trade_buy(crypto_currency=crypto_currency, amount=num)
		else:
			success, received, remains, funds, order_id = trade_buy(crypto_currency=crypto_currency, amount=num, rate=rate)	

		output = ""

		if success:
			output += "Транзакция прошла успешно \n"
			output += "ID транзакции: {} \n".format(order_id)
			output += "Получено: {} {} \n".format(received, crypto_currency.upper())
			output += "Оставшийся объем: {} {} \n".format(received, crypto_currency.upper())
			output += "Баланс: \n"
			for name, count in funds:
				output += " " + name + ": " + str(count) + "\n"
		else:
			output += "Ошибка транзакции \n"
			output += "На счете недостаточно средств \n"

		bot.send_message(message.from_user.id, output)

		buy_a = None

		return True
	return False

inp = False

@bot.message_handler(func=lambda message: True)
def send(message):

	global crypto_currency
	global currency
	global buy_a
	global sell_a
	global rate
	global inp

	# buy_a
	# True: Я буду покупать по обычной цене
	# False: Я хочу попробовать купить по своей цене

	if "/info" not in message.text:

		if message.text == 'Я буду покупать по обычной цене':
			buy_a = True
			bot.send_message(message.from_user.id, "Какое количество?")
			return
		elif message.text == 'Я хочу попробовать купить по своей цене':
			bot.send_message(message.from_user.id, 'Какая цена (в долларах)?')
			inp = True
			return

		if transaction(message):
			return
		else:
			if inp == True:
				rate = float(message.text)
				buy_a = False
				inp = False
				transaction(message)
				return 
			markup = types.ReplyKeyboardMarkup()
			button1 = types.KeyboardButton("Я буду покупать по обычной цене")
			button2 = types.KeyboardButton("Я хочу попробовать купить по своей цене")
			markup.row(button1)
			markup.row(button2)
			bot.send_message(message.from_user.id, "Как будешь покупать?", reply_markup=markup)


		for cur, name in get_currency_list():
			if message.text == cur + "-" + name:
				currency = message.text.split('-', 1)[0]
				if current == 'info':
					main(message)
				return

		try:
			crypto_currency = message.text
			for crypto in get_crypto_currency_list():
				if crypto.lower() == crypto_currency.lower():
					markup = types.ReplyKeyboardMarkup()
					for cur, name in get_currency_list():
						button = types.KeyboardButton(cur + "-" + name)
						markup.row(button)
					if current == 'info':
						bot.send_message(message.from_user.id, "Выбери валюту:", reply_markup=markup)
					break
		except:
			pass

bot.polling()
