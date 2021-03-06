# -*- coding: utf-8 -*-

from telebot import types


def add_keyboard(cities_dict: dict):
    """
    Функция добавления клавиатуры
    :param cities_dict: Dict. Словарь где ключ - Навзание страны и название города, значение - айди отеля
    :return: ReplyKeyboardMarkup. Клавиатура для выбора нужного города
    """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i_city in cities_dict:
        key = types.KeyboardButton(i_city)
        keyboard.add(key)

    return keyboard


def keyboard_for_get_photo_answer():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes = types.KeyboardButton('Да')
    key_no = types.KeyboardButton('Нет')
    keyboard.add(key_yes, key_no)

    return keyboard
