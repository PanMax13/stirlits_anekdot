from bs4 import BeautifulSoup as bs
import requests
from conf import token
import aiogram
from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import  ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,     InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime

import random
import linecache



url = 'https://anekdoty.ru/pro-shtirlica/'
bot = Bot(token)
db = Dispatcher(bot)

response = requests.get(url)
soup = bs(response.text, 'lxml')



# check what is month now to update anekdots.txt 

date_today = datetime.now().strftime("%B")

with open('anek.txt', 'a+') as file:
    if file.readline() == date_today:
        
        anekdotes = soup.find_all('div', class_ = 'holder-body')
        file.truncate(0)
        file.write(date_today + '\n')
        for anek in anekdotes:
            file.write(anek.text + '\n')

        print("Month changed")
        file.close()
    else:
        print("all good")




# bot settings

button = KeyboardButton("Анекдот")
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(button)

@db.message_handler(commands = ['start'])
async def start(message):
    await bot.send_message(message.from_user.id, "Привет, анекдот?", reply_markup=kb)
    

@db.message_handler(lambda message: message.text == "Анекдот")
async def send_anekdot(message):
    with open('anek.txt') as file:
        lines = file.readlines()
    
    random_anek = random.choice(lines)[:-1]
     

    await bot.send_message(message.from_user.id, random_anek, reply_markup=kb) 
    print(message.from_user.id)
executor.start_polling(db) 
