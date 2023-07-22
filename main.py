from telebot import types
import telebot
from config import TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
import config

bot = telebot.TeleBot(TOKEN)
bot_username = bot.get_me().username

# Запись в Базу Данных
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    if message.from_user.username == None:
        bot.send_message(chat_id, ' Вам необходимо установить логин для работы с ботом!')
    else:
        func.first_join(user_id=chat_id, username=username)
        bot.send_message(chat_id, '💳Вот лучшие займы для вас: \n\n🔥Займер - https://clck.ru/354EJw \n0%, от 2000₽, от 7 дней \n\n💵MoneyMan - https://clck.ru/354EQS \n0% от 3000₽, от 3 дней \n\n👑Webbankir - https://clck.ru/354ETe \n0%, от 2000₽, от 7 дней ', parse_mode="Markdown", reply_markup=kb.menu)

# Вызов Админ Панели
@bot.message_handler(commands=['admin'])
def start(message: types.Message):
    if message.chat.id == admin:
        bot.send_message(message.chat.id, ' {}, вы авторизованы!'.format(message.from_user.first_name),
                         reply_markup=kb.admin)
#Функции бота
@bot.callback_query_handler(func=lambda call: True)   
def handler_call(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'statistics':
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=func.stats(), reply_markup=kb.admin)
    elif call.data == 'message':
        msg = bot.send_message(chat_id=chat_id,
                               text='Введите текст для рассылки. \n\nДля отмены напишите "-" без кавычек!')
        bot.register_next_step_handler(msg, message1)
def message1(message):
    text = message.text
    if message.text.startswith('-'):
        bot.send_message(message.chat.id, text=canel_operation)
    else:
        info = func.admin_message(text)
        bot.send_message(message.chat.id, text=' Рассылка начата!')
        for i in range(len(info)):
            try:
                time.sleep(1)
                bot.send_message(info[i][0], str(text))
            except:
                pass
        bot.send_message(message.chat.id, text=' Рассылка завершена!')
        print (info)
# Поддержание работы
bot.polling(none_stop=True)
bot.infinity_polling()
