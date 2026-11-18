import telebot
import os

BOT_API_KEY = os.environ.get("BOT_API_KEY")

bot = telebot.TeleBot(BOT_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    print('start')
    bot.send_message(message.chat.id, '<b>Hi.</b> I\'m ready to start.', parse_mode='HTML')

bot.polling(non_stop=True, interval=0)