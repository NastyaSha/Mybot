def dz1(bot, message):
    txt_message = f"Имя: {message.from_user.first_name}"
    bot.send_message(message.chat.id, text=txt_message, )


# -----------------------------------------------------------------------
def dz2(bot, message):
    txt_message = message.from_user.first_name
    t = 3 * txt_message
    bot.send_message(message.chat.id, text=t)


# -----------------------------------------------------------------------


# -----------------------------------------------------------------------

def dz4(bot, message, types):
    markup = types.InlineKeyboardMarkup(row_width=2)
    itg = types.InlineKeyboardButton('больше 18', url='https://www.youtube.com/watch?v=M-5ZkrA1REM')
    itgg = types.InlineKeyboardButton('меньше 18', url='https://www.youtube.com/watch?v=sHfh4BhUqNg')

    markup.add(itg, itgg)
    bot.send_message(message.chat.id, "Нажми на свой возраст", reply_markup=markup)


# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def dz6(bot, message):
    bot.send_message(message.chat.id,
                     f"Добро пожаловать {message.from_user.first_name}! У тебя красивое имя, в нём {len(message.from_user.first_name)} букв!")

