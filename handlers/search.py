"""
Модуль содержит обработчики, осуществляющие поиск зарегистрированных
пользователей в базе данных BigQuery, по команде /search.
"""
from aiogram.types import Message
from loader import dp
from states.search_states import SearchStates
from re import compile, fullmatch
from utils import db

db_manager = db.DBManager()


@dp.message_handler(commands=["search"], state="*")
async def search_info(message: Message) -> None:
    """
    Обработчик осуществляет приветствие и информирует о
    правилах поиска пользователей.
    """
    await message.answer(
        "Что бы найти информацию о зарегистрированном пользователе введите: "
        "Фамилию, Имя, корпоративную почту (@ylab.io) или telegram-логин "
        "(в формате @username).\n"
        "Вы можете ввести всю известную информацию одним сообщением, в любом "
        "порядке, отделяя слова пробелами, а так же можете ввести "
        "произвольное число слов в одном сообщении, например только Фамилию и "
        "Имя или только telegram-логин.\n"
        "Примеры запросов:\nГригорий Гуляев g.gulyaev@ylab.io @icedevil\n"
        "Григорий Гуляев\nГуляев\ng.gulyaev@ylab.io")
    await SearchStates.SEARCH_PROCESS.set()


@dp.message_handler(state=SearchStates.SEARCH_PROCESS)
async def search_response(message: Message) -> None:
    """
    Обработчик принимает поисковый запрос от пользователя,
    и отправляет сообщение в чат с результатом поиска.
    """
    parse_data = parsing(message.text)
    if isinstance(parse_data, str):
        await message.answer(parse_data)
    else:
        await message.answer(users_search(parse_data))


def parsing(data: str) -> any:
    """
    Функция принимает поисковый запрос от пользователя и осуществляет его
    парсинг, таким образом, что функция возвращает словарь, ключи которого
    соответствуют названиям полей базы данных BigQuery.

    parse_data= {'email': 'gemail@ylab.io',
                 'telegram_name': '@username',
                 'full_name': ['имя', 'фамилия']}

    В случае ввода неверных данных (is_valid = False) функция
    отправит пользователю в чат сообщение об ошибке.

    :param data: "cырые" данные вытянутые из сообщения пользователя
    :type data: str.data

    :retype: -> any
    """
    data: list = data.split()
    parse_data: dict = {'full_name': 'str', 'email': 'str',
                        'telegram_name': 'str'}
    words: list = []
    for word in data:
        if 'ylab.io' in word:
            if is_data_valid(word, 'email'):
                parse_data.update({'email': word})
            else:
                return "Проверьте правильность электронной почты!"
        elif '@' in word:
            if is_data_valid(word, 'telegram_name'):
                parse_data.update({'telegram_name': word})
            else:
                return "Проверьте правильность @username или @email!"
        else:
            words.append(word.lower().capitalize())
            if is_data_valid(" ".join(words), 'full_name'):
                parse_data.update({'full_name': words})
            else:
                return "Проверьте правильность Имени и Фамилии!"
    return parse_data


def is_data_valid(data: str, case: str) -> bool:
    """
    Функция принимает строки и сопоставляет их с регулярными выражениями,
    возвращает True в случае соответствия.

    :param data: спарсенные слова
    :type data: str.parse_data

    :param case: типа шаблона
    :type case: str

    :rtype: bool

    is_nice = True
    state = "nice" if is_nice else "not nice"

    """
    re_telegram = compile(r"@+[a-zA-Z0-9_]{5,64}")
    re_email = compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@ylab.io")
    re_text = compile(
        r"[а-яА-ЯёЁa-zA-Z]+\s+[а-яА-ЯёЁa-zA-Z]+|[а-яА-ЯёЁa-zA-Z]{2,32}")
    return True if \
        (case == 'telegram_name' and fullmatch(re_telegram, data)) or \
        (case == 'email' and fullmatch(re_email, data)) or \
        (case == 'full_name' and fullmatch(re_text, data)) else False


def users_search(parse_data: dict) -> str:
    """
    Функция принимает структурированные данные и использует их как ключи,
    для осуществления поиска в подключенной SQL-БД, который осуществляется
    при вызове функции get_df_for_search(). Найденные данные отправляются
    пользователю в чат.

    :param parse_data: структурированные данные
    :type parse_data: dict.parse_data

    :rtype: str
    """
    frame_data = db_manager.get_df_for_search(parse_data)
    search_answer = frame_data.to_dict(orient="index")
    if search_answer:
        for index in search_answer:
            if len(parse_data['full_name']) != 2:
                return view(search_answer)
            elif match(search_answer[index], parse_data):
                return " ".join(list(search_answer[index].values()))
            else:
                return view(search_answer)
    else:
        return "Пользователь не существует или данные введены не корректно!"


def view(data: dict) -> str:
    """
    Функция принимает найденные данные в формате dict и
    преобразовывает их в строки для отправки пользователю.

    :param data: найденная информация в БД
    :type data: dict['str', str']

    :rtype: str
    """
    answer = '\n'.join([' '.join(data[index].values()) for index in data])
    return answer


def match(search_answer: dict, parse_data: dict) -> bool:
    """
    Если пользователь найден и по имени и по фамилии, одновременно, то функция
    вернет True и в таком случае другие найденные совпавшие имена и
    фамилии выведены не будут.

    :param search_answer: найденная информация
    :type search_answer: dict[str, str]

    :param parse_data: структурированные данные
    :type parse_data: dict[str, str]

    :rtype: bool
    """
    s_name = search_answer['fullname'].split()
    p_name = parse_data['full_name']
    if s_name[0] == p_name[0] and s_name[1] == p_name[1] or \
            s_name[0] == p_name[1] and s_name[1] == p_name[0]:
        return True
    else:
        return False
