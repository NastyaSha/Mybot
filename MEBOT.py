import json
from gettext import find
from io import BytesIO
from glob import glob
from random import choice
import random
import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4  # beautifulsoup4
from menuBot import Menu
import DZ  # домашнее задание от первого урока

bot = telebot.TeleBot('5107163046:AAHB3P8SnKdwdB5kLyC7XWXjMVCBkVCKD54')


@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет, {message.from_user.first_name}! Отдохни!"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


def show_map(gmap):
    gmap_width = str(gmap.find(u'█\n') + 1)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn = types.InlineKeyboardButton(u'⬆', callback_data='-' + gmap_width)
    btn3 = types.InlineKeyboardButton(u'➡', callback_data='1')
    btn2 = types.InlineKeyboardButton(u'⬅', callback_data='-1')
    btn4 = types.InlineKeyboardButton(u'⬇', callback_data=gmap_width)
    markup.add(btn3, btn4, btn2, btn)

    return {
        'text': '<code>' + gmap + '</code>',
        'parse_mode': 'HTML',
        'reply_markup': markup
    }


@bot.message_handler(commands=['game'])
def any_msg(message):
    gmap = u"""
    ██████████
    █. ███ . █
    █  ©☿©   █
    █  ©   .██
    ██████████
 """
    bot.send_message(message.chat.id, **show_map(gmap))


def replace_on_map(game_map, pos, char):
    return game_map[:pos] + char + game_map[pos + 1:]


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        gmap = call.message.text
        movement = int(call.data)

        pos = gmap.find(u'☿')
        if pos < 0:
            pos = gmap.find(u'♆')

        new_pos = pos + movement
        new_place = gmap[new_pos]
        next_place = gmap[new_pos + movement]

        if new_place in (' ', '.') or (new_place in (u'©', u'о') and next_place in (' ', '.')):
            if new_place in (u'©', u'о'):
                gmap = replace_on_map(gmap, new_pos + movement, u'о' if next_place == '.' else u'©')
            gmap = replace_on_map(gmap, pos, ' ' if gmap[pos] == u'☿' else '.')
            gmap = replace_on_map(gmap, new_pos, u'☿' if new_place in (' ', u'©') else u'♆')

        if gmap != call.message.text:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                **show_map(gmap)
            )


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)
    if result == True:
        return

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "HELP🍓":
            send_help(chat_id)

        elif ms_text == "Поддержка🌸":
            cool(chat_id)

        elif ms_text == "Анекдот🍓":
            bot.send_message(message.chat.id, text=anus())

        elif ms_text == "Картинки🌸":
            cartin(chat_id)

        elif ms_text == "Гадалка💖":
            bot.send_message(chat_id, text="✨✨✨Подождите! Я читаю вашу ауру !✨✨✨")
            getcat(chat_id)

        elif ms_text == "Задание-1":
            DZ.dz1(bot, message)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, message)

        elif ms_text == "Задание-3":
            DZ.dz6(bot, message)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, message, types)



        elif ms_text == "Совет💖":
            valu(chat_id)

        elif ms_text == "Baka🌸":
            ggg(chat_id)

        elif ms_text == "Аниме фильмы💖":
            film(chat_id)









    else:
        bot.send_message(chat_id, text="Проверь туда ли ты нажал(а)?: " + ms_text)
        goto_menu(chat_id, "Главное меню")


# ------------------------
def goto_menu(chat_id, name_menu):
    if name_menu == "Назад" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        return True
    else:
        return False


# -----------------------------------------------------------------------
def send_help(chat_id):
    bot.send_message(chat_id, "Автор:Анастасия Шалабанова")
    key1 = types.InlineKeyboardMarkup()
    me = types.InlineKeyboardButton("Напишите автору", url='https://t.me/nast345')
    key1.add(me)
    img = open("F:\АНА.jpg", "rb")
    bot.send_photo(chat_id, img, reply_markup=key1)


# -----------------------------------------------------------------------
def anus():
    array_anekdot = []
    req_ane = requests.get('https://4tob.ru/anekdots/tag/black')
    so = bs4.BeautifulSoup(req_ane.text, 'html.parser')
    resu = so.select('.text')
    a = random.randint(0, 29)
    for resul in resu:
        array_anekdot.append(resul.getText().strip())
    return array_anekdot[a]


# -----------------------------------------------------------------------
def cool(chat_id):
    key1 = types.InlineKeyboardMarkup()
    cat = types.InlineKeyboardButton(text="КОТИКИ", url='https://www.youtube.com/watch?v=tdSc8DfS_8Q')
    music = types.InlineKeyboardButton(text="Послушай музыку",
                                       url='https://youtube.com/playlist?list=PL393S3SzgmBwkCXb1iCvdzTEagWBqKm77')
    pie = types.InlineKeyboardButton(text="Приготовь пирог",
                                     url='https://youtu.be/3hA5yrzkgIQ')
    med = types.InlineKeyboardButton(text="Медитация",
                                     url='https://www.youtube.com/watch?v=9Him1Sd9pEc')
    test = types.InlineKeyboardButton(text="Пройди тесты",
                                      url='https://suzzy.ru/page/2/')
    film = types.InlineKeyboardButton(text="Фильмы",
                                      url='https://www.filmpro.ru/materials/selections')
    key1.add(cat, music, pie, med, test, film)
    bot.send_message(chat_id, "Ты хорошо сегодня поработал(а)! Используй эти кнопки, чтобы расслабиться! ",
                     reply_markup=key1)

    # ----------------------------------------------------------------------


def cartin(chat_id):
    lists = glob('F:\Питон\imga/*')
    poc = choice(lists)
    bot.send_photo(chat_id, photo=open(poc, 'rb'))


# -----------------------------------------------------------------------
def getcat(chat_id):
    with open("F:\Таро.txt", "rb") as f:
        lines = f.readlines()
        lists = ['F:\\Питон\\Карты\\0.jpg', 'F:\\Питон\\Карты\\1.jpg', 'F:\\Питон\\Карты\\2.jpg',
                 'F:\\Питон\\Карты\\3.jpg', 'F:\\Питон\\Карты\\4.jpg', 'F:\\Питон\\Карты\\5.jpg',
                 'F:\\Питон\\Карты\\6.jpg', 'F:\\Питон\\Карты\\7.jpg', 'F:\\Питон\\Карты\\8.jpg',
                 'F:\\Питон\\Карты\\9.jpg', 'F:\\Питон\\Карты\\10.jpg', 'F:\\Питон\\Карты\\11.jpg',
                 'F:\\Питон\\Карты\\12.jpg', 'F:\\Питон\\Карты\\13.jpg', 'F:\\Питон\\Карты\\14.jpg',
                 'F:\\Питон\\Карты\\15.jpg', 'F:\\Питон\\Карты\\16.jpg', 'F:\\Питон\\Карты\\17.jpg',
                 'F:\\Питон\\Карты\\18.jpg']

        a = random.randint(0, 19)
        tet1 = lists[a]
        tet = lines[a]
    bot.send_message(chat_id, text=tet)
    bot.send_photo(chat_id, photo=open(tet1, 'rb'))
    print(a)


def valu(chat_id):
    con = requests.get("https://api.adviceslip.com/advice").json()
    p = con["slip"]
    bot.send_message(chat_id, p["advice"])


def valu(chat_id):
    con = requests.get("https://api.adviceslip.com/advice").json()
    p = con["slip"]
    bot.send_message(chat_id, p["advice"])


def ggg(chat_id):
    con = requests.get("https://api.catboys.com/baka").json()
    img = con["url"]
    bot.send_video(chat_id, img, None, 'Text')


def film(chat_id):
    con = requests.get("https://ghibliapi.herokuapp.com/films/").json()
    i = random.randint(0, 20)
    p = con[i]
    bot.send_message(chat_id,
                     "✨"+p['title']+"✨" + '\n' + p['original_title'] + '\n' + p['release_date'] + '\n' + p['description'])
    bot.send_photo(chat_id, p["movie_banner"])


bot.polling(none_stop=True)
