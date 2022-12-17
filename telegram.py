# telebot.types.InlineKeyboardMarkup 
# telebot.types.InlineKeyboardButton
# @bot.callback_query_handler(func= lambda call: True)
import os
import telebot
import random

bot = telebot.TeleBot("5712136718:AAFw57oSZdrj8ptT2ytxmm3O5O38gCrOlh4")


PATH = os.path.abspath(__file__ + '/..') + '/image/'
dir2 = os.listdir(PATH)
dir1 = []
for i in dir2:
    dir1.append(int(i.split('.')[0]))
dir1.sort()
NUM_FILE = dir1[-1]
keyboard = telebot.types.InlineKeyboardMarkup()
btn1 = telebot.types.InlineKeyboardButton('add photo', callback_data= 'add')
btn2 = telebot.types.InlineKeyboardButton('get photo', callback_data= 'get')
keyboard.add(btn1, btn2)
@bot.message_handler(commands=["start"])
def start(message):
    
    bot.send_message(message.chat.id, 'select options', reply_markup=keyboard)

@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    global NUM_FILE
    if call.data == 'add':
        msg = bot.send_message(call.message.chat.id, 'Send photo')
        bot.register_next_step_handler(msg, upload_photo)
    elif call.data == 'get':
        n = random.randint(1,NUM_FILE)
        with open(f'{PATH}{str(n)}.png', 'rb') as f:
            bot.send_photo(call.message.chat.id, f,  reply_markup=keyboard)
def upload_photo(message):
    global NUM_FILE
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, 'I have got your photo',  reply_markup=keyboard)
        file = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file.file_path)
        NUM_FILE += 1
        print(NUM_FILE)
        with open(f'{PATH}{str(NUM_FILE)}.png', 'wb') as f:
            f.write(file)
    else:
        msg = bot.send_message(message.chat.id, 'Error: Send photo')
        bot.register_next_step_handler(msg, upload_photo)
@bot.message_handler(commands=['select'])
def select_photo(message):
    global NUM_FILE
    reply_key = telebot.types.ReplyKeyboardMarkup(row_width=4)
    for i in range(NUM_FILE):
        btn = telebot.types.KeyboardButton(f'{str(i + 1)}.png')
        reply_key.add(btn)
    msg = bot.send_message(message.chat.id, 'Select photo file', reply_markup = reply_key)
    bot.register_next_step_handler(msg, get_photo)
def get_photo(message):
    with open(PATH + message.text, 'rb') as f:
        msg = bot.send_photo(message.chat.id, f,  reply_markup=telebot.types.ReplyKeyboardRemove())
        
bot.polling(non_stop=True)