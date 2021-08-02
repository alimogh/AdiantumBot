import telebot

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.from_user.id, 
		"Привет, я могу прислать тебе котенка. Если хочешь - пиши /cat"
	)

@bot.message_handler(commands=['cat'])
def send_cat(message):
	cat = open('cat.png', 'rb')
	bot.send_message(message.from_user.id, 
		"Нет, лучше посмотри что такое КУБИТ"
	)
	bot.send_photo(message.from_user.id, cat)

bot.polling()