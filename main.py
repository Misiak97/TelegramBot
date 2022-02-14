import re
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, date
from telebot import types
from loguru import logger
from dotenv import load_dotenv
from models import *
from History import *
from user import User
import settings
from keybord import add_keyboard
from botrequests import best_deal_request, lowprice_request, city_req, photo_req


load_dotenv()
logger.add(settings.logger_settings[0], format=settings.logger_settings[1], level=settings.logger_settings[2])

bot = telebot.TeleBot(settings.token)

with db:
    LastSearch.create_table()


@bot.message_handler(commands='start')
def start(message):
    """
    Функция запуска чата с ботом, в которой выводится приветствие и создается или подтягивается экземляр класса
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    bot.send_message(user.id, f'Здравтсвуйте, {user.name}!\n{settings.start_message}\n{settings.commands}')
    logger.info(f'Пользователь {user.username} ввел команду "/start"')


@bot.message_handler(commands='help')
def helping_commands(message):
    """
    Функция для отправки пользователю всех доступных боту команд
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    user.user_command = '/help'
    bot.send_message(user.id, f'Список команд:\n{settings.commands}')
    logger.info(f'Пользователь {user.username} ввел команду "/help"')


@bot.message_handler(commands='lowprice')
def lowprice(message):
    """
    Функция запускающая процесс поиска самых дешевых отелей, в которой атрибутам
    экземляра пользователя присваивается введенная им команда и фильтр для сортировки
    и запросом нужного пользователю города
    :param message: Сообщение отправленное пользователем
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    user.user_command = 'lowprice'
    user.command_time = datetime.now()
    user.user_filter = 'PRICE'
    user.hotels = list()
    bot.send_message(user.id, 'Введите название города, в котором искать отель:')
    logger.info(f'Пользователь {user.username} ввел команду "/lowprice"')
    bot.register_next_step_handler(message, first_city_appropriator)


@bot.message_handler(commands='highprice')
def highprice(message):
    """
    Функция запускающая процесс поиска самых дорогих отелей, в которой атрибутам
    экземляра пользователя присваивается введенная им команда и фильтр для сортировки и отправкой сообщения
    с запросом нужного пользователю города
    :param message: Сообщение отправленное пользователем
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    user.user_command = 'highprice'
    user.command_time = datetime.now()
    user.hotels = list()
    user.user_filter = 'PRICE_HIGHEST_FIRST'
    bot.send_message(user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, first_city_appropriator)
    logger.info(f'Пользователь {user.username} ввел команду "/highprice"')


@bot.message_handler(commands='bestdeal')
def bestdeal(message):
    """
    Функция запускающая процесс поиска отелей по кретериям расстояния от центра и диапозону стоимости, которые
    в дальнейшем будут введены пользователем, в которой атрибутам экземляра пользователя присваивается
    введенная им команда для сортировки и отправкой сообщения с запросом нужного пользователю города
    :param message: Сообщение отправленое пользователем
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    user.user_command = 'bestdeal'
    user.command_time = datetime.now()
    user.hotels = list()
    bot.send_message(user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, first_city_appropriator)
    logger.info(f'Пользователь {user.username} ввел команду "/bestdeal"')


@bot.message_handler(commands='history')
def history(message):
    """
    Функция для отправки пользователю истории его поиска хронящуюся в базе данных
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    for i_info in LastSearch.select().where(LastSearch.user_id == user.id):
        bot.send_message(user.id, f'Команда: {i_info.command}\n'
                                  f'Время ввода команды: {i_info.command_time}\n'
                                  f'Отели:\n{i_info.hotels}'
                         )


@bot.message_handler(content_types='text')
def first_city_appropriator(message):
    """
    Функция получения от пользователя названия необходимого ему города с проверкой на ввод, и парсером списка всех
    городов с данным названием
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    if message.text in settings.commands_list:
        bot.send_message(user.id, 'Запрос приостановлен. Вот список доступных комманд \n{}'.format(settings.commands))
        breakpoint()
    city = message.text.title()
    pattern = re.compile(settings.normal_symbols)
    checking_city = pattern.search(city) is not None
    logger.info(f'Пользователь {user.username} ввел город {city}')

    if checking_city:

        found_cities = city_req.id_city_selection(city)

        if len(found_cities) != 0:
            user.city = found_cities
            my_keyboard = add_keyboard(user.city)
            bot.send_message(user.id, 'Выберите нужный город', reply_markup=my_keyboard)
            bot.register_next_step_handler(message, city_id_identification)
        else:
            bot.send_message(user.id, 'К сожалению я не смог найти введенный вами город, проверьте правильность ввода и'
                                      'введите нужную вам команду заново')
            logger.info(f'Город не найден')
    else:
        bot.send_message(user.id, 'Пожалуйста, проверьте правильность введенного вами'
                                  ' города и введите название еще раз!')
        logger.info(f'Была допущена орфографическая ошибка в названии города')
        bot.register_next_step_handler(message, first_city_appropriator)


@bot.message_handler(content_types='text')
def city_id_identification(message):
    """
    Функция коллбэк для обработки нажатия пользователем кнопки выбора нужного ему города, которая присваивает айди этого
    города атрибуту класса пользователя
    :param message:
    :return:
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)

    try:
        user.city_id = user.city[message.text]
        logger.info(f'Пользователем {user.username} был выбран {user.city_id} айди города')
        bot.send_message(user.id, 'Введите кол-во отелей для поиска:', reply_markup=types.ReplyKeyboardRemove(),
                         parse_mode='Markdown')
        bot.register_next_step_handler(message, hotels_atm_changer)
    except BaseException as err:
        bot.send_message(user.id, 'Вам нужно выбрать город из списка, путем нажатия, а не сообщения в чат')
        logger.debug(f'{err}: Пользователь {user.username} написал в чат, вместо выбора города из списка')
        bot.register_next_step_handler(message, city_id_identification)


@bot.message_handler(content_types='text')
def hotels_atm_changer(message):
    """
    Функция присваивания атрибуту класса пользователя кол-ва отелей для поиска с обработкой исключения если пользователь
    ввел неверное значение
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    try:
        user.hotels_atm = int(message.text)
        if int(user.hotels_atm) < 0:
            bot.send_message(user.id, 'Число не может быть отрицательным, попробуйте еще раз')
            bot.register_next_step_handler(message, hotels_atm_changer)
        logger.info(f'Пользователем {user.username} было выбрано {user.hotels_atm} отелей')
        arrival(message)
    except ValueError as err:
        bot.send_message(user.id, 'Ожидалась число, проверьте ввод и попробуйте снова!')
        logger.error(f'{err}: Ошибка, пользователем введено неверное значение')
        bot.register_next_step_handler(message, hotels_atm_changer)


def arrival(message):
    """
    Функция для создания календаря в виде инлайн клавиатуры для выбоа пользователем даты заезда
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)

    calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=date(2022, 1, 1),
                                              max_date=date(2025, 12, 31)).build()
    logger.info(f'Пользователь {user.username} выбирает дату заселения')
    bot.send_message(user.id,
                     f'Выберете дату заезда {LSTEP[step]}',
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal1(call):
    """
    Коллер для получения результата нажатий кнопок календаря даты заезда пользователем
    """
    date_today = date.today()
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите дату заезда', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        if date_today > result:
            bot.edit_message_text('Дата заезда не может быть раньше текущей даты, попробуйте снова',
                                  call.message.chat.id, call.message.message_id)
            arrival(call.message)
        else:
            bot.edit_message_text(f'Введенная дата заезда {result}',
                                  call.message.chat.id, call.message.message_id
                                  )
            user = User.get_user(call.message.chat.id, call.message.chat.first_name, call.message.chat.username)
            user.arrival_date = str(result)

            date_of_departure(call.message)


def date_of_departure(message):
    """
    Функция для создания календаря в виде инлайн клавиатуры для выбоа пользователем даты выезда
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)

    calendar, step = DetailedTelegramCalendar(calendar_id=2, locale='ru', min_date=date(2022, 1, 1),
                                              max_date=date(2025, 12, 31)).build()
    logger.info(f'Пользователем {user.username} выбирает дату выезда')
    bot.send_message(user.id,
                     f'Выберете дату выезда {LSTEP[step]}',
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def cal2(call):
    """
     Коллер для получения результата нажатий кнопок календаря даты выезда пользователем
     """
    result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите дату выезда', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        user = User.get_user(call.message.chat.id, call.message.chat.first_name, call.message.chat.username)

        if user.arrival_date < str(result):
            bot.edit_message_text(f'Введенная дата выезда {result}',
                                  call.message.chat.id, call.message.message_id
                                  )
            user.date_of_departure = str(result)

            if user.user_command in ['lowprice', 'highprice']:
                loads_photo_choice(call.message)
            elif user.user_command == 'bestdeal':
                hotel_price(call.message)
        else:
            bot.edit_message_text('Дата выезда не может быть раньше даты заезда, попробуйте снова',
                                  call.message.chat.id, call.message.message_id)
            date_of_departure(call.message)


@bot.message_handler(content_types='text')
def hotel_price(message):
    """
    Функция запроса минимальной и максимальной допустимой, для пользователя, стоимости отелей, которые
    в дальнейшем используются для поиска
    :param message: Сообщение от полльзователя
    :return:
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    bot.send_message(user.id, 'Введите мин/макс стоимость через пробел')
    logger.info(f'Пользователь {user.username} вводит мин/макс стоимость отелей за сутки')
    bot.register_next_step_handler(message, price_saver)


@bot.message_handler(content_types='text')
def price_saver(message):
    """
    Функция присваивания экземпляру класса пользователя двух атрибутов с минимальной и максимальной стоюмостью отелей,
    для дальнейшего поиска, с обработкой ошибки, если пользователь перепутал местами значения
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    price = message.text.split()
    try:
        user.min_price, user.max_price = int(price[0]), int(price[1])
        if int(user.min_price) > int(user.max_price):
            user.min_price, user.max_price = user.max_price, user.min_price
            bot.send_message(user.id, 'Кажется вы перепутали местами мин/макс стоимость, '
                                      'но ничего, я самостоятельно все исправил!'
                             )
        bot.send_message(user.id, 'Введите оптимальное для вас расстояние в Км. от центра.')
        logger.info(f'Пользователь {user.username} вводит расстояние отеля от центра')
        bot.register_next_step_handler(message, distance_to_center)
    except ValueError as err:
        logger.error(f'Ошибка:{err}\nПользователь {user.name} ввел неверное значение цены')
        bot.send_message(user.id, 'Ошибка ввода цены, проверьте правильность и попробуйте снова')
        bot.register_next_step_handler(message, price_saver)
    except IndexError as sec_err:
        logger.error(f'Ошибка:{sec_err}\nПользователь не ввел второе число')
        bot.send_message(user.id, 'Ошибка, кажется вы забыли ввести второе число.Попробуйте снова')
        bot.register_next_step_handler(message, price_saver)


@bot.message_handler(content_types='text')
def distance_to_center(message):
    """
    Функция присваивания экземпляру класса пользователя атрибута введеной пользователем предпочтительной дистанции от
    центра с обработкой исключения и выводом пользователю ошибки, если она была произведена
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    try:
        distance = int(message.text)
        user.distance = distance
        loads_photo_choice(message)
        logger.info(f'Пользователь {user.username} ввел предпочтительную дистанцию от центра')
    except ValueError as err:
        bot.send_message(user.id, 'Ожидалось число, проверьте ввод и попробуйте снова')
        logger.error(f'{err}: Пользователем введено неверное значение, ожидалось число')
        bot.register_next_step_handler(message, distance_to_center)


@bot.message_handler(content_types='text')
def loads_photo_choice(message):
    """
    Функция запроса необходимы ли пользователю фотографии отеля
    :param message:
    :return:
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    bot.send_message(user.id, 'Нужны ли фото?')
    logger.info(f'Пользователь {user.username} вводит отевет')
    bot.register_next_step_handler(message, photos)


@bot.message_handler(content_types='text')
def photos(message):
    """
    Функция получающая сообщения от пользователя с ответом, необходимы ли фотографии отелей и в зависимости от
    результата ответа вызывает другую функцию, прежде присваивая атрибуту экземпляра пользователя булево значение
    :param message: Сообщение полученое от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    answer = message.text
    if answer.title() == 'Да':
        user.photos_answer = True
        bot.send_message(user.id, 'Сколько фото загрузить (Не более 10)?')
        logger.info(f'Пользователь {user.username} вводит кол-во фото для загрузки')
        bot.register_next_step_handler(message, number_of_photo)
    elif answer.title() == 'Нет':
        user.photos_answer = False
        hotels_atm_choicer(message)
    else:
        bot.send_message(user.id, 'Извините, я вас не понял, пожалуйста, введите "Да" или "Нет"!')
        logger.info(f'Пользователь {user.username} ввел неверный ответ на вопрос о загрузке фото')
        bot.register_next_step_handler(message, photos)


@bot.message_handler(content_types='text')
def number_of_photo(message):
    """
    Функция получающая в сообщение от пользователя кол-во фото для загрузки, с обработкой исключения в случае, если
    пользователем введен неподдерживаемое значение
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    try:
        photos_counter = int(message.text)
        user.photos_atm = photos_counter
        hotels_atm_choicer(message)
    except ValueError as err:
        logger.error(f'{err}: Пользователем введено неверное значение, ожидалось число')
        bot.send_message(user.id, 'Ожидалось число, пожалуйста, проверьте ввод и попробуйте еще раз!')
        bot.register_next_step_handler_by_chat_id(user.id, number_of_photo)


def hotels_atm_choicer(message):
    """
    Функция парсер, получающая список отелей в зависимости от комманды введенной пользователем со встроенным парсером
    фотографий отеля (если они имеются), которая объеденияет каждый отель с фотографиями и отправляет их пользователю
    :param message: Сообщение от пользователя
    """
    user = User.get_user(message.chat.id, message.chat.first_name, message.chat.username)
    bot.send_message(user.id, 'Пожалуйста подождите, подбираю отели по вашему запросу!')
    hotels = None

    try:
        if user.user_command in ['lowprice', 'highprice']:
            hotels, user.hotels = lowprice_request.lowprice_req(user.city_id, user.hotels_atm, user.user_filter,
                                                                user.arrival_date, user.date_of_departure
                                                                )

        elif user.user_command == 'bestdeal':
            hotels, user.hotels = best_deal_request.bestdeal_req(user.city_id, user.hotels_atm,
                                                                 user.arrival_date, user.date_of_departure,
                                                                 user.distance, user.min_price, user.max_price)

        bot.send_message(user.id, f'По вашему запрусу было найдено {len(hotels)} отелей')

        for i_hotel, i_hotel_info in hotels.items():
            hotel = f'{i_hotel}\n{"".join(i_hotel_info[:-1])}\nСсылка на отель: ' \
                    f'https://ru.hotels.com/ho{i_hotel_info[-1]}'
            bot.send_message(user.id, hotel)
            if user.photos_answer:
                hotel_id = i_hotel_info[-1]
                media = photo_req.get_photo(hotel_id, user.photos_atm)
                if type(media) == str:
                    bot.send_message(user.id, media)
                else:
                    bot.send_media_group(user.id, media=media)

        check_history(user.name, user.id, user.user_command, user.command_time, user.hotels)

    except AttributeError as err:
        logger.error(f'{err}: По запросу пользователя не было найдено отелей')
        bot.send_message(user.id, 'К сожалению по вашему запросу не удалось найти отели')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
