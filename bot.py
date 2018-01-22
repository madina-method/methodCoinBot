#import config
import time
import telebot
from telebot import types
#import db
#from telebot.types import ShippingOption
import datetime
import math
import requests as r

bot = telebot.TeleBot("522023702:AAFNNOLXYIId_GN78AW7i3NPUytD-ghTT3k")
username = ""
main_buttons = ['Мои монеты', 'Присвоить монету', 'Красавчики']
karmas = ['+1', '-1']
names = ["Samat", "Yerdos", "Bota", "Alibek", "Aigerim", "Aruzhan", "Madina", "Gaziza", "Aidana"]
nicknames = ["isamat", "Yoridosu", "Bota13", "alibek2017", "zhunussova", "Aru071", "madina_tj", "ga3iza", "AidLeps"]
newnames = []
ids = []
coins = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global username
    username = message.chat.username
    welcome_msg = "Привет, *{0}*. Что будем делать? ".format(message.chat.first_name)
    bot.send_message(message.chat.id, welcome_msg, reply_markup=create_keyboard(words=main_buttons,width=1), parse_mode='markdown')
    

   
@bot.message_handler(content_types=['text'])
def handle_message(message):
    global username
    username = message.chat.username
    chat_id = message.chat.id
    if message.text == "Мои монеты":
        
        #welcome_msg = "Введи свой ID: ".format(message.chat.first_name)
        #msg = bot.send_message(message.chat.id, welcome_msg)
        #bot.register_next_step_handler(msg, myCoins)
        myCoins(username, chat_id)
    elif message.text == "Присвоить монету":
        welcome_msg = "Берем или Отбираем?"
        msg = bot.send_message(message.chat.id, welcome_msg, reply_markup=create_keyboard(words=karmas, width=2), parse_mode='markdown')
        bot.register_next_step_handler(msg, karmaDef)
    elif message.text == "Красавчики":

            welcome_msg = ""
        
            dataAll = r.get("http://madina.mthd.kz/get_leaders.php").text.strip()
            dataAll = dataAll[:len(dataAll)-1]
            users_array = dataAll.split(";")
            users_count = len(users_array)

            top_users = []
            top_coins = []
            counter = 1
            for user in users_array:
                sp_user = user.split(":")
                welcome_msg += str(counter)+" место. "+sp_user[0] + " - "+str(sp_user[1])+"\n"
                counter+=1

            msg = bot.send_message(message.chat.id, welcome_msg, reply_markup=create_keyboard(words=main_buttons, width=2), parse_mode='markdown')

def karmaDef(message):
    global username
    for i in range(len(names)):
        if nicknames[i] != username:
            newnames.append(names[i])
    welcome_msg = "Выбери коллегу: ".format(message.chat.first_name)
    msg = bot.send_message(message.chat.id, welcome_msg, reply_markup=create_keyboard(words=newnames, width=2), parse_mode='markdown')

    if message.text == "+1":
        bot.register_next_step_handler(msg, giveCoin)
    elif message.text == "-1":
        bot.register_next_step_handler(msg, getCoin)



def myCoins(username, chat_id):    
        found = False
        ids, coins= getDb()
        for i in range(len(ids)):
            if ids[i]==username:
                if int(coins[i]) == 0:
                    dopMessage = "Опасная зона. Вы можете уйти в минус. Делайте больше добрых дел."
                    bot.send_message(chat_id, "В вашей копилке "+ str(coins[i])+" methodCoins.\n"+dopMessage)
                else:
                    bot.send_message(chat_id, "В вашей копилке "+ str(coins[i])+" methodCoins.")
                found = True
                break
        #if not found:
            #bot.send_message(message.chat.id, "Упс, кажется неправильный ID. \nНажмите заново 'Мои монеты'.")   


def giveCoin(message):
    username2 = message.text
    findDb("plus", username2, message.chat.id)
def getCoin(message):
    username2 = message.text
    findDb("minus", username2, message.chat.id)
    

def create_keyboard(words=None, width=None, isOneTime=False, isPhone=False):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=isOneTime, row_width=width, resize_keyboard = True)
    for word in words:
        keyboard.add(types.KeyboardButton(text=word, request_contact=isPhone))
    return keyboard

def getDb():

    dataAll = r.get("http://madina.mthd.kz/log_teen.php").text.strip()
    dataAll = dataAll[:len(dataAll)-1]
    users_array = dataAll.split(";")
    users_count = len(users_array)

    ids = []
    coins = []

    for user in users_array:
        sp_user = user.split(":")
        ids.append(sp_user[0])
        coins.append(sp_user[1])
    return ids, coins

def findDb(sign, username, chat_id): 
    link = ""
    welcome_msg = ""   
    if sign == "plus":
        link = "http://madina.mthd.kz/update_teen.php?username="+username  
        welcome_msg = "Какие мы добрые сегодня =)"   
    elif sign == "minus":
        link = "http://madina.mthd.kz/update_teen2.php?username="+username
        welcome_msg = "В мире грустит один методошник =( "   

    data = r.get(link)

    msg = bot.send_message(chat_id, welcome_msg, reply_markup=create_keyboard(words=main_buttons,width=1),parse_mode='markdown')



ids, coins= getDb()

if __name__ == '__main__':
    bot.polling(none_stop=True)
