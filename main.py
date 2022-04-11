from email import message
from glob import glob
from random import *
import re
import sqlite3
from tkinter.tix import Tree
from urllib import request
import telebot
from telebot import types


global db
global sql
db = sqlite3.connect('dates.db', check_same_thread=False)
sql = db.cursor()
loop = 1
bot = telebot.TeleBot('5174908248:AAH0SVVFd7li0n9Jo_yWJzgg3XoTyFHnNK8')

login = ''
password = ''


# створення БД
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT,
    dick BEINT
)""")
db.commit()



@bot.message_handler(commands=['start'])
def welocome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Вирощувати пісюна')
    item2 = types.KeyboardButton('Інформація')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, '''
Вітаю, я написав гру "Вирости пісюна". 
Ти можеш її потестувати та повеселитися. 
Слава Україні! ''', reply_markup=markup)


# створення профіля та занесення в БД
def request_login(message):
    global login
    login = message.text

    bot.send_message(message.chat.id, 'Ваш пароль: ')    
    bot.register_next_step_handler(message, request_password)


def request_password(message):
    global login, password
    password = message.text
    print(login, password)    
    user_login, user_password = login, password

    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")    
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
        db.commit()
        bot.send_message(message.chat.id, 'Ви зареєстували свій акаунт!')
    
    else:
        bot.send_message(message.chat.id, 'Такий акаунт вже існує!')
        bot.register_next_step_handler(message, log_in)


# вхід у БД
def log_in(message):
    global login, password
    login = message.text

    bot.send_message(message.chat.id, 'Окей, увідіть ваш пароль: ')
    bot.register_next_step_handler(message, pass_in)


def pass_in(message):
    global login, password
    user_login  = login
    user_password = message.text
    
    '''Якщо такого користувача немає в БД, то ми його відправляємо на реєстацію
    Якщо ж ні, то він є в БД та ми граємо гру'''
    
    for i in sql.execute(f"SELECT dick FROM users WHERE login = '{user_login}'"):
        balance = i[0]    
    sql.execute(f'SELECT login, password FROM users WHERE login = "{user_login}" AND password = "{user_password}"')
    if sql.fetchone() is None:
        bot.send_message(message.chat.id, 'Такого гравця не існує. Зареєструйтеся!\nВаш логін: ')
        bot.register_next_step_handler(message, request_login)

    else:
        # рандомне значення, яке буде генеруватися
        dick_heigth = randint(-20, 20) 
        
        # взалежності від знаку числа, виводити різні повідомлення. Проте значення оновлювати в БД
        if dick_heigth > 0:
            bot.send_message(message.chat.id, 'Вітаю, '+str(user_login)+' ваш пісюн збільшився на '+str(dick_heigth)+' см.')
            
            # оновлення значень
            sql.execute(f'UPDATE users SET dick = {dick_heigth + balance} WHERE login = "{user_login}"')
            db.commit()
            
        elif dick_heigth < 0:
            bot.send_message(message.chat.id, 'Вітаю, '+str(user_login)+' ваш пісюн зменшився на '+str(dick_heigth)+' см.')
            sql.execute(f'UPDATE users SET dick = {dick_heigth + balance} WHERE login = "{user_login}"')
            db.commit()

        else:
            bot.send_message(message.chat.id, 'Вітаю, '+str(user_login)+' ваш пісюн незмінився.')
            sql.execute(f'UPDATE users SET dick = {dick_heigth + balance} WHERE login = "{user_login}"')
            db.commit()
    
  

# оброботчик подій
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == '1':
        bot.send_message(call.message.chat.id, 'Ваш логін: ')
        bot.register_next_step_handler(call.message, request_login)
    
    elif call.data == '2':
        '''я створюю локанльний список та закидаю в нього вложений список із ім*ям та значенням в породку спадання
        через цикл ФОР я перепираю його значення та виводжу в телеграм'''
        top_list = []
        for i in sql.execute('SELECT login, dick FROM users'):
            template_list = []
            template_list.append(i[1])
            template_list.append(i[0])
            top_list.append(template_list)

        top_list.sort(reverse=True)
        number_of_repeat = len(top_list)
        index_list = 0
        while number_of_repeat > index_list:
            bot.send_message(call.message.chat.id, str(index_list+1)+' місце: '+str(top_list[index_list][1])+' із '+str(top_list[index_list][0])+'см пісюнa.')
            index_list += 1
    
    elif call.data == '3':
        bot.send_message(call.message.chat.id, 'В грі на данний момент зареєствровані такі користувачі:')
        for i in sql.execute('SELECT login FROM users'):
            bot.send_message(call.message.chat.id, i[0])        

    elif call.data =='4':
        bot.send_message(call.message.chat.id, 'Пробуємо зайти.\nУведіть ваш логін: ')
        bot.register_next_step_handler(call.message, log_in)
    
    elif call.data == '0':
        bot.send_message(call.message.chat.id, 'ще не придумав, як виходити.\nМоже маєш варіанти?')

    else:
        bot.send_message(call.message.chat.id, 'Щось пішло не так під час вибору дії!')



@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Вирощувати пісюна':
            
            # створюю інлайнові кнопки, які будуть кріпитися що такого-то повідомлення
            state_game = types.InlineKeyboardMarkup(row_width=2)
            button_1 = types.InlineKeyboardButton('1. Зареєстуватися', callback_data='1')        
            button_2 = types.InlineKeyboardButton('2. Топ всіх гравців', callback_data='2')    
            button_3 = types.InlineKeyboardButton('3. Які гравці є?', callback_data='3')    
            button_4 = types.InlineKeyboardButton('4. Грати пісюна', callback_data='4')    
            button_0 = types.InlineKeyboardButton('0. Вихід', callback_data='0')    

            state_game.add(button_1, button_2, button_3, button_4, button_0)
            bot.send_message(message.chat.id, 'Ну що ж, будемо вирощувати пісюни\nВиберіть дію: ', reply_markup=state_game)
                      
        elif message.text == 'Інформація':
            information = '''Щодня у світі ламаються пісюни від необережного використання. 
Ваші розміри пісюна ніяк не пов*язані з довжиною стопи.
Пісюн - це не м*яз.''' 
            bot.send_message(message.chat.id, information)           
           


bot.polling(none_stop=True)