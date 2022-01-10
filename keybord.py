from telebot import types


def add_keyboard(cities_dict):
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
