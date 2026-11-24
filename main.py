
import telebot
import os
from random import choice, randint

BOT_API_KEY = os.environ.get("BOT_API_KEY")
bot = telebot.TeleBot(BOT_API_KEY)

# Store individual user sessions
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "<b>Hi.</b> I'm ready to start.",
        parse_mode="HTML"
    )


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "/start - Start bot\n"
        "/start_test - Start a test\n"
        "/stop - Stop test"
    )


@bot.message_handler(commands=['start_test'])
def start_test(message):
    print(users)
    users[message.chat.id] = {
        "state": "difficulty",
        "minimum": None,
        "maximum": None,
        "answer": None
    }
    print(users)

    bot.send_message(
        message.chat.id,
        'Select a difficulty:\n'
        '1 - Easy\n'
        '2 - Medium\n'
        '3 - Hard'
    )


def create_test(chat_id):
    user = users[chat_id]

    num1 = randint(user["minimum"], user["maximum"])
    num2 = randint(user["minimum"], user["maximum"])

    operation = choice(['+', '-', '*'])

    match operation:
        case '+':
            answer = num1 + num2
        case '-':
            answer = num1 - num2
        case '*':
            answer = num1 * num2

    user["answer"] = answer
    user["state"] = "answer"

    if num2 < 0:
        bot.send_message(
            chat_id,
        f"What is {num1} {operation} ({num2})?"
        )
    else:
        bot.send_message(
            chat_id,
            f"What is {num1} {operation} {num2}?"
        )


@bot.message_handler(commands=['stop'])
def stop(message):
    users.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Test stopped.")


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in users:
        return

    user = users[chat_id]

    # Difficulty selection
    if user["state"] == "difficulty":

        difficulties = {
            "1": (1, 39),
            "2": (1, 139),
            "3": (-50, 300)
        }

        if text not in difficulties:
            bot.send_message(chat_id, "Please select 1, 2 or 3.")
            return

        user["minimum"], user["maximum"] = difficulties[text]

        create_test(chat_id)

    # Answer checking
    elif user["state"] == "answer":

        try:
            user_answer = int(text)
        except ValueError:
            bot.send_message(chat_id, "Please enter a number.")
            return

        if user_answer == user["answer"]:
            bot.send_message(chat_id, "Correct! Well done.")
        else:
            bot.send_message(
                chat_id,
                f"Incorrect! The answer was {user['answer']}."
            )

        create_test(chat_id)


bot.infinity_polling()
