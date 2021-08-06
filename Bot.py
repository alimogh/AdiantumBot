import telebot
from telebot import types
from Helper import *
import json

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

USER_KEY = None
USER_SECRET = None

current = ''

bot = telebot.TeleBot(API_TOKEN)

buy_a = None
sell_a = None

inp_token = False

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
	global current, inp_token
	inp_token = False
	current = 'info'
	bot.send_message(message.from_user.id, "Какая криптовалюта?", reply_markup=types.ReplyKeyboardRemove())

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

@bot.message_handler(commands=['sell'])
def sell(message):
	global inp_token
	global USER_KEY
	global USER_SECRET

	data = open("database.txt", 'r').readlines()
	for line in data:
		if str(message.from_user.id) in line:
			if USER_KEY is None:
				USER_KEY = str(line.split(':', 1)[1])
			elif USER_SECRET is None:
				USER_SECRET = str(line.split(':', 1)[1])

	if USER_KEY is None or USER_SECRET is None:
		bot.send_message(message.from_user.id, "Мне нужен твои ключи биржы YoBit.net")
		bot.send_message(message.from_user.id, "Раздел 'API ключи' в личном кабинете. \n Нужно сгенерировать ключ с правами 'info & trade & deposits' и отправить их мне через пробел")
		bot.send_message(message.from_user.id, "Пример: fe4riuh34iu34rh3i4ruhf34iuhg 239fj85r9jef98u4439p8ij6g5978")
		inp_token = True
		return
	global current
	current = 'sell'
	bot.send_message(message.from_user.id, "Какая криптовалюта?", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['buy'])
def buy(message):
	global inp_token
	if USER_KEY is None or USER_SECRET is None:
		bot.send_message(message.from_user.id, "Мне нужен твои ключи биржы YoBit.net")
		bot.send_message(message.from_user.id, "Раздел 'API ключи' в личном кабинете. \n Нужно сгенерировать ключ с правами 'info & trade & deposits' и отправить их мне через пробел")
		bot.send_message(message.from_user.id, "Пример: fe4riuh34iu34rh3i4ruhf34iuhg 239fj85r9jef98u4439p8ij6g5978")
		inp_token = True
		return
	global current
	current = 'buy'
	bot.send_message(message.from_user.id, "Какая криптовалюта?", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['cat'])
def send_cat(message):
	global currentinp_token
	inp_token = False
	cat = open('cat.png', 'rb')
	bot.send_message(message.from_user.id, 
		"Нет, лучше посмотри что такое КУБИТ", reply_markup=types.ReplyKeyboardRemove()
	)
	bot.send_photo(message.from_user.id, cat, reply_markup=types.ReplyKeyboardRemove())

def transaction(message):

	global crypto_currency
	global currency
	global buy_a
	global sell_a
	global sell_a
	global rate
	global num

	print(buy_a, sell_a)

	if buy_a is not None or sell_a is not None:
		success = False
		received = 0
		remains = 0
		funds = 0

		if buy_a is not None:
			if buy_a:
				success, received, remains, funds, order_id = trade_buy(crypto_currency=crypto_currency, amount=num)
			else:
				success, received, remains, funds, order_id = trade_buy(crypto_currency=crypto_currency, amount=num, rate=rate)	

		if sell_a is not None:
			if sell_a:
				success, received, remains, funds, order_id = trade_sell(crypto_currency=crypto_currency, amount=num)
			else:
				success, received, remains, funds, order_id = trade_sell(crypto_currency=crypto_currency, amount=num, rate=rate)

		output = ""

		print(success, received, remains, funds, order_id)

		if success:
			output += "Транзакция прошла успешно \n"
			output += "ID транзакции: {} \n".format(order_id)
			if buy_a is not None:
				output += "Куплено: {} {} \n".format(received, crypto_currency.upper())
			else:
				output += "Продано: {} {} \n".format(received, crypto_currency.upper())
			output += "Оставшийся объем торгов: {} {} \n".format(received, crypto_currency.upper())
			output += "Баланс: \n"
			for name, count in funds:
				output += " " + name + ": " + str(count) + "\n"
		else:
			output += "Ошибка транзакции \n"
			if buy_a is not None:
				output += "На счете недостаточно средств \n"
			elif sell_a is not None:
				output += "На балансе недостаточно криптовалюты \n"

		bot.send_message(message.from_user.id, output, reply_markup=types.ReplyKeyboardRemove())

		buy_a = None
		sell_a = None

		return True
	return False

inp = False
inp_num = False

num = 0

@bot.message_handler(func=lambda message: True)
def send(message):

	global crypto_currency
	global currency
	global buy_a
	global sell_a
	global rate
	global inp
	global inp_token
	global USER_KEY, USER_SECRET
	global inp_num
	global num

	# buy_a
	# True: Я буду покупать по обычной цене
	# False: Я хочу попробовать купить по своей цене

	# sell_a
	# True: Я буду продавать по обычной цене
	# False: Я хочу попробовать продать по своей цене

	if "/info" not in message.text and '/' not in message.text:

		if inp_num:
			num = float(message.text)
			inp_num = False
			transaction(message)
			return

		if inp_token:
			USER_KEY, USER_SECRET = message.text.split()
			setup(USER_KEY, USER_SECRET)
			try:
				response = balance()
				success, funds, funds_incl_orders, transaction_count, open_orders = response
				if success:
					bot.send_message(message.from_user.id, "Успешная авторизация") 
					with open('database.txt', 'w') as f:
						f.write("{}:{}\n".format(str(message.from_user.id), str(USER_KEY)))
						f.write("{}:{}\n".format(str(message.from_user.id), str(USER_SECRET))) 
					output = ""
					if type(funds) is not int:
						output += "Баланс: \n"
						for name, count in funds:
							output += " " + name + ": " + str(count) + "\n"
					else:
						output += "Баланс: 0\n"
					bot.send_message(message.from_user.id, output)
					inp_token = False
				else:
					bot.send_message(message.from_user.id, "Ошибка авторизации - Несуществуюшие ключи")
					inp_token = True
			except:
				bot.send_message(message.from_user.id, "Ошибка авторизации - Несуществуюшие ключи")
				inp_token = True
			

		if message.text == 'Я буду продавать по обычной цене':
			sell_a = True
			bot.send_message(message.from_user.id, "Какое количество?", reply_markup=types.ReplyKeyboardRemove())
			inp_num = True
			return
		if message.text == 'Я буду покупать по обычной цене':
			buy_a = True
			bot.send_message(message.from_user.id, "Какое количество?", reply_markup=types.ReplyKeyboardRemove())
			inp_num = True
			return
		elif message.text == 'Я хочу попробовать купить по своей цене' or message.text == 'Я хочу попробовать продать по своей цене':
			bot.send_message(message.from_user.id, 'Какая цена (в долларах)?', reply_markup=types.ReplyKeyboardRemove())
			inp = True
			return

		if transaction(message):
			return
		else:
			if inp == True:
				rate = float(message.text)
				if buy_a is None:
					buy_a = False
				elif sell_a is None:
					sell_a = False
				inp = False
				bot.send_message(message.from_user.id, "Какое количество?", reply_markup=types.ReplyKeyboardRemove())
				inp_num = True
				return
			if current == 'buy':
				markup = types.ReplyKeyboardMarkup()
				button1 = types.KeyboardButton("Я буду покупать по обычной цене")
				button2 = types.KeyboardButton("Я хочу попробовать купить по своей цене")
				markup.row(button1)
				markup.row(button2)
				bot.send_message(message.from_user.id, "Как будешь покупать?", reply_markup=markup)
			elif current == 'sell':
				markup = types.ReplyKeyboardMarkup()
				button1 = types.KeyboardButton("Я буду продавать по обычной цене")
				button2 = types.KeyboardButton("Я хочу попробовать продать по своей цене")
				markup.row(button1)
				markup.row(button2)
				bot.send_message(message.from_user.id, "Как будешь продавать?", reply_markup=markup)

		for cur, name in get_currency_list():
			if message.text == cur + "-" + name:
				currency = message.text.split('-', 1)[0]
				if current == 'info':
					send_info(message)
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
