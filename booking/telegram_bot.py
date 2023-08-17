import telebot
from dotenv import load_dotenv, dotenv_values
from .models import CarNote

env_keys = dotenv_values()
RISOLA_CAR_BOT_TOKEN = env_keys.get('RISOLA_CAR_BOT_TOKEN')
bot = telebot.TeleBot(token=RISOLA_CAR_BOT_TOKEN)

DAY = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}


# bot.send_message(chat_id='-1001977048993', text='Xaxaxa')
#
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     bot.send_message(message.from_user.id, "!11")
#     bot.send_message(chat_id='-1001977048993', text=message.text)


def say_in_chat(note: CarNote, message=''):
    if message:
        bot.send_message(chat_id='-1001977048993',
                         text=f'_---{message}---_\n*{DAY[note.date.weekday()]}* {note.date}\n{note.car} - {note.city}\n{note.engineer}',
                         parse_mode='Markdown')
    else:
        bot.send_message(chat_id='-1001977048993',
                         text=f'*{DAY[note.date.weekday()]}* {note.date}\n{note.car} - {note.city}\n{note.engineer}',
                         parse_mode='Markdown')

# bot.polling(none_stop=True, interval=0)
