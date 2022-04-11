from cgitb import text
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('5174908248:AAH0SVVFd7li0n9Jo_yWJzgg3XoTyFHnNK8')
name = ''
surname = '' 
age = 0

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'ми стартанули')


@bot.message_handler(content_types=['text'])
def answer(message):
    
    if message.text == '/reg':
        bot.send_message(message.chat.id, 'ми реєструємося\nВаше ім*я: ')
        bot.register_next_step_handler(message, reg_name)
    
    else:
        bot.send_message(message.chat.id, message.text)



def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Ваше прізвище: ')
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, 'Ваш вік: ')
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age 
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, 'Пиши цифрами вік: ')
    
    bot.register_next_step_handler(message, print_reg)

def print_reg(message):
    date_user = [name, surname, age]
    print(date_user)
    bot.send_message(message, 'Реєстація закінчена!')



bot.polling(none_stop=True)

# що я хочу? щоб забрати у користувача дані, які він увів