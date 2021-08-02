import telebot

API_TOKEN = '1949911063:AAF-IxP5jIwNFAIG_Pr_9o5VnDvawvUlq5Y'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Хай дюд")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()