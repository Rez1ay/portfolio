# телеграм бот для интернет магазина автотоваров


import telebot
from telebot import types


TOKEN = ''  # токен бота
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])    # приветственное сообщение + кнопки
def welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website = types.KeyboardButton('Наш магазин')   # кнопки
    info = types.KeyboardButton('О нас')
    contacts = types.KeyboardButton('Контакты')
    catalog = types.KeyboardButton('Каталог')
    markup.add(website, contacts, catalog, info)
    bot.send_message(message.chat.id, 'Welcome', reply_markup=markup)  # приветственное сообщение

    with open('Контакты.txt', 'r+') as f:   # запись id написавших пользователей, для последующей рассылки
        if str(message.chat.id) not in f.read():
            print(message.chat.id, file=f)


@bot.message_handler(func=lambda message: message.text == 'Наш магазин')    # ссылки на магазин
def website_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Avito', url='https://www.avito.ru'))
    markup.add(types.InlineKeyboardButton('Юла', url='https://youla.ru'))
    markup.add(types.InlineKeyboardButton('VK', url='https://vk.com'))
    bot.send_message(message.chat.id, 'Посетите наш магазин!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'О нас')
def info_message(message):
    bot.send_message(message.chat.id, 'Магазин автотоваров')


@bot.message_handler(func=lambda message: message.text == 'Контакты')
def contacts_message(message):
    bot.send_message(message.chat.id, 'Номер для связи: 8(123)456-78-90 \n'
                                      'Адрес: Москва')


@bot.message_handler(func=lambda message: message.text == 'Каталог')
def catalog_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Автомагнитолы', callback_data='radio'))
    markup.add(types.InlineKeyboardButton(text='Динамики', callback_data='sound'))
    markup.add(types.InlineKeyboardButton(text='Автоаксессуары', callback_data='acces'))
    markup.add(types.InlineKeyboardButton(text='Другое', callback_data='other'))
    bot.send_message(message.chat.id, 'Каталог товаров', reply_markup=markup)


# папка каталог создается в папке с ботом, туда закидываются папки соответствующими категориями (сейчас их 4),
# затем создаются папки с конкретным товаром и называются от 0 до 10 (можно увеличить)
# в папке с товаром содержится по одному .jpg и .txt файла с названиями 'Фото' и 'Описание' соответственно

@bot.callback_query_handler(func=lambda call: True)
def callback_catalog(call):
    bot.send_message(call.message.chat.id, 'Секундочку, отправляю Вам каталог товаров')
    if call.data == 'radio':
        for i in range(10):
            try:
                photo = open(f'Каталог/Магнитолы/{i}/Фото.jpg', 'rb')
                text = open(f'Каталог/Магнитолы/{i}/Описание.txt', encoding='utf-8')
                bot.send_photo(call.message.chat.id, photo, text.read())
            except Exception:
                pass

    elif call.data == 'sound':
        for i in range(10):
            try:
                photo = open(f'Каталог/Динамики/{i}/Фото.jpg', 'rb')
                text = open(f'Каталог/Динамики/{i}/Описание.txt', encoding='utf-8')
                bot.send_photo(call.message.chat.id, photo, text.read())
            except Exception:
                pass

    elif call.data == 'acces':
        for i in range(10):
            try:
                photo = open(f'Каталог/Автоаксессуары/{i}/Фото.jpg', 'rb')
                text = open(f'Каталог/Автоаксессуары/{i}/Описание.txt', encoding='utf-8')
                bot.send_photo(call.message.chat.id, photo, text.read())
            except Exception:
                pass

    elif call.data == 'other':
        for i in range(10):
            try:
                photo = open(f'Каталог/Другое/{i}/Фото.jpg', 'rb')
                text = open(f'Каталог/Другое/{i}/Описание.txt', encoding='utf-8')
                bot.send_photo(call.message.chat.id, photo, text.read())
            except Exception:
                pass
    bot.send_message(call.message.chat.id, 'Готово! Если вас что-то заинтересовало, '
                                           'звоните по номеру 8(123)456-78-90 или посетите наш сайт!')


@bot.message_handler(commands=['spam'])  # отправка рассылки по команде /spam
def spam(message):
    if message.chat.id == 000000000:    # id админа
        bot.send_message(message.chat.id, 'отправьте рассылку')
        bot.register_next_step_handler(message, send_spam)  # фото + текст или текст, который отправиться в виде рассылки
    else:
        bot.send_message(message.chat.id, 'у вас недостаточно прав')


def send_spam(message):
    if message.content_type == 'photo':
        photo = message.photo[0].file_id
        text = message.caption
        with open('Контакты.txt') as file:  # отправка пользователям, id которых содержиться в файле 'Контакты'
            for i in file:
                bot.send_photo(int(i), photo, text)

    elif message.content_type == 'text':
        text = message.text
        with open('Контакты.txt') as file:
            for i in file:
                bot.send_message(int(i), text)

    else:
        bot.send_message(message.chat.id, 'нужно отправлять текст или фото с текстом')


@bot.message_handler(func=lambda m: True)  # стандартный ответ
def answer_message(message):
    bot.send_message(message.chat.id, 'Не понимаю вас')


bot.polling(none_stop=True)
