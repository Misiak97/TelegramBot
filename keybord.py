from telebot import types


def add_keyboard(cities_dict):
    """
    ������� ���������� ����������
    :param cities_dict: Dict. ������� ��� ���� - �������� ������ � �������� ������, �������� - ���� �����
    :return: ReplyKeyboardMarkup. ���������� ��� ������ ������� ������
    """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i_city in cities_dict:
        key = types.KeyboardButton(i_city)
        keyboard.add(key)

    return keyboard
