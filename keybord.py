from telebot import types


def add_keyboard(cities_dict):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i_city in cities_dict:
        key = types.KeyboardButton(i_city)
        keyboard.add(key)

    return keyboard
