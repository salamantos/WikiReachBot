# coding=utf-8

# Настраиваемые параметры бота

# Exceptions


class FatalError(Exception):
    def __int__(self, text):
        FatalError.txt = text


class EasyError(Exception):
    def __int__(self, text):
        EasyError.txt = text


class ContinueError(Exception):
    def __int__(self, text):
        ContinueError.txt = text


# BOT_TOKEN = '353206446:AAEnwupmsYWkapfe3RLjRmCbJ4ZN_NNYJww'  # salamantos_first_bot
BOT_TOKEN = '312320944:AAHRVs-an8Jy0iTl9Q5sfzwPfv8GrwKuLV4'  # WikiReachBot

URL_PREFIX = u'https://ru.wikipedia.org'  # https://ru.wikipedia.org/wiki/Кошка
SEARCH_TEMPLATE_PREFIX = u'https://ru.wikipedia.org/w/index.php?search='
SEARCH_TEMPLATE_POSTFIX = u'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F%3A%D0' \
                          u'%9F%D0%BE%D0%B8%D1%81%D0%BA&go=%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D1%82' \
                          u'%D0%B8 '

MAX_LINKS_COUNT = 200
# Если MAX_MESSAGES_COUNT или меньше, выводим полностью
MAX_MESSAGES_COUNT = 3
# Если больше MAX_MESSAGES_COUNT, выводим первые SPLIT_MESSAGES_COUNT и спрашиваем, нужно ли еще
SPLIT_MESSAGES_COUNT = 2

TIMEOUT_PERSONAL_MESSAGES = 1  # seconds
BIG_TIMEOUT_PERSONAL_MESSAGES = 80

MAX_MESSAGE_SIZE = 4096

DEFAULT_DIFFICULTY = 4

DIFFICULTY_LIST = {
    u'Hard\n(3 перехода)': 3,
    u'Normal\n(4 перехода)': 4,
    u'Easy\n(5 переходов)': 5
}

KEYBOARD = [
    [u'Hard\n(3 перехода)', u'Normal\n(4 перехода)', u'Easy\n(5 переходов)'],
    [u'Отмена']
]

BLACK_LIST = [u'Редактировать раздел', u'Википедия', u'Ссылки на источники',
              u'(Страница отсутствует)', u'(страница отсутствует)',
              u'Просмотр этого шаблона', u'Служебная:', u'Шаблон:', u'Увеличить', u'Ethnologue']

# Dictionary
NO_TEXT = u'Вы не написали текста, сударь o_O'
NON_EXISTENT_COMMAND = u'Такой команды нет :с'
THIS_IS_LINKS_LIST = u'Вот список ссылок по статье '
YOUR_GOAL_IS = u'\n(Вам нужно дойти до статьи\n'
WHAT_YOU_WANT_TO_CHOOSE = u'Напишите номер выбранной ссылки'
GOAL_ARTICLE_WAS_CHANGED = u'Целевая статья успешно изменена на '
ENTER_ARTICLE_LINK = u'Введите название статьи или ссылку на неё'
CONGRATULATIONS = u'Поздравляю, вы победили за '
STEPS = u' ходов!'
NO_MORE_STEPS = u'У вас закончились ходы, но статья '
NOT_REACHED = u' не достигнута'
NO_LINKS_IN_CHOSEN_ARTICLE = u'Вы проиграли! Выбрана статья без ссылок :((('
STEPS_MADE = u'\n\nУже сделано ходов: '
HELLO_AT_START = u'Привет! Справка по командам: /help'
GAME_ALREADY_STARTED = u'Вы уже начали игру :)'
GIVE_ANSWER = u'Вы не ответили на вопрос, ну'
YOU_NOT_PLAY = u'Вы не играете сейчас в игру'
GAME_STOPPED = u'Игра завершена'
CANT_CHANGE_ARTICLE_WHILE_PLAYING = u'Нельзя сменить целевую статью во время игры'
INVITE_TO_START = u'Хотите начать игру?\nНаберите /start_game или посмотрите /help для ' \
                  u'справки по командам'
WRONG_ENTERED_URL = u'Ссылка не работает, попробуйте снова'
OPENING_JUST_WHILE_PLAYING = u'Открыть статью можно только во время игры'
WRONG_ID = u'Неверный номер'
CANT_CHANGE_DIFFICULTY_WHILE_PLAYING = u'Нельзя сменить сложность во время игры'
DIFFICULTY_WAS_CHANGED = u'Сложность успешно изменена на '
WRONG_ENTERED_DIFFICULTY = u'Плез, выберите верное значение на появившейся клавиатуре'
SELECT_DIFFICULTY = u'Выберите сложноть на появившейся клавиатуре'
SELECTING_DIFFICULTY_CANCELED = u'Отменено, вы можете начать игру: /start_game'
COMMANDS_HELP = u'''Справка по командам:\n
/rules - Узнать правила игры
/help - Помощь по командам
/start_game - Начать игру
/end_game - Закончить текущую игру
/answer - ответить (нужно для групповых чатов): answer <Ваш ответ>
/change_article - Выбрать статью, до которой нужно добраться
/hitler_mode - REACH HITLER!
/set_difficulty - Настроить сложность игры
/open - Открыть статью в Википедии'''
RULES = [u'''Привет!
Правила очень простые:
# Я выдаю вам все ссылки из случайной статьи Википедии
# Ваша задача - переходя по этим ссылкам дойти до целевой статьи
# Целевая статья назвается ''',
         u''' (её можно сменить)
# Количество ходов ограничено: нужно уложиться в ''',
         u''' переходов (тоже можно поменять)
# Собственно, всё :D

P.S. Не пугайтесь, если ссылок больше 1000, это нормально))''']
SCORE1 = u'Игр сыграно: '
SCORE2 = u'\nВы победили в '
SCORE3 = u' из них'
OPEN_TO_GET_LINK = u'Введите номер статьи из списка'
YOU_CANCELED_ARTICLE = u'Вы отменили выбор'
ARTICLES_FOUND = u'Найденные статьи:\n'
SELECT_ARTICLE_OR_CANCEL = u'\nВыберите нужную или наберите cancel для отмены'
CHOOSE_OR_NEED_MORE = u'Показана часть ссылок. Напишите номер выбранной ссылки или more, ' \
                      u'чтобы загрузить еще'
MORE_LINKS = u'Еще ссылки:\n'

# entities=[MessageEntity(type=u'bold', offset=0, length=3, url=None, user=None)]

RANDOM_PAGE_LINK = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6' \
                   '%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87' \
                   '%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0' \
                   '%D0%BD%D0%B8%D1%86%D0%B0 '

DEFAULT_ARTICLE_URL = 'https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F'
DEFAULT_ARTICLE_HEADER = u'Россия'

HITLER_ARTICLE_URL = 'https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D1%82%D0%BB%D0%B5%D1%80,' \
                     '_%D0%90%D0%B4%D0%BE%D0%BB%D1%8C%D1%84 '
HITLER_ARTICLE_HEADER = u'Гитлер, Адольф'

# Error prefixes:
# ut - update type - Если пришло не сообщение
