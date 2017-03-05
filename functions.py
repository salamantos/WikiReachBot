# coding=utf-8

import time
from twx.botapi import TelegramBot
from bs4 import BeautifulSoup
import urllib2

import settings
from storage import Storage


# Модуль логов
# -------------------------------------------------------------------------
def sys_time():
    return time.time()


def log_write(scenario, action, log_time, user='', log_user_id=''):
    tuple_time = time.gmtime(log_time)
    # log_time = int(log_time)
    res_time = time.strftime('%Y-%m-%d %H:%M:%S', tuple_time)
    if scenario == 'usr':
        log_file.write(
            str(res_time) + ': @' + str(user) + ' (' + str(log_user_id) + ') написал: "' + str(action) + '"\n')
    elif scenario == 'bot':
        log_file.write(
            str(res_time) + ': ---> @' + str(user) + ' (' + str(log_user_id) + ') бот ответил: "' + str(action) +
            '"\n')
    elif scenario == 'sys':
        log_file.write(str(res_time) + ': ' + str(action) + '\n')
    elif scenario == 'endl':
        log_file.write('\n')


# Модуль запросов к Телеграму
# -------------------------------------------------------------------------
def recognize_update(update_object):
    update_id = update_object.update_id
    received_user_id = update_object.message.sender.id
    received_username = update_object.message.sender.username
    # chat_id = update_object.message.chat.id
    # chat_type = update_object.message.chat.type  # Пока работаем с приватным, проверить
    request_date = update_object.message.date
    received_text = update_object.message.text

    return update_id, received_user_id, received_username, received_text, request_date


def answer(bot, send_user_id, send_answer_text='Это пустое сообщение'):
    result = bot.send_message(send_user_id, send_answer_text).wait()
    log_write('bot', result, sys_time())


def init_bot(init_token):
    bot = TelegramBot(init_token)
    bot.update_bot_info().wait()
    return bot


def get_updates_for_bot(bot, offset):
    return bot.get_updates(offset).wait()


# Модуль запросов к Википедии
# -------------------------------------------------------------------------

def open_link(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Достаем данные о текущей статье
    current_page_link = soup.find(rel="canonical").get('href')
    current_page_header = soup.find(id="firstHeading").get_text()
    print('Current Link is ' + current_page_link)
    print('Current Page is ' + str(current_page_header) + '\n')

    soup = soup.find(id="mw-content-text")
    a = soup.find_all('a')

    result = []
    for link in a:
        try:
            href = link.get('href')
            title = link.get('title')
            # inner_html = link.get_text()

            if not ('https' in href) and not (title is None):
                next_link = False
                for black_word in settings.black_list:
                    if black_word in title:
                        next_link = True
                    if 'img' in str(link):
                        next_link = True
                if not next_link:
                    result.append([title, href])
        except TypeError:
            log_write('sys', 'EMPTY HREF!!!', sys_time())  # Не происходит из-за проверки not (title is None)
    return result


def init_game():
    link_to_open = settings.random_page_link
    return open_link(link_to_open)


# Модуль комманд бота
# -------------------------------------------------------------------------
# Порядок аргументов: session_continues, storage, user_id, username

def c_help(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return u'Справка по командам:'


def c_start_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    if storage.data[user_id]['state'] == 'waitForStart':
        storage.data[user_id]['state'] = 'game'
        return 'init_game()'
    elif storage.data[user_id]['state'] == 'game':
        return u'Вы уже начали игру :)'
    else:
        return u'Ответьте на вопрос, плез'


def c_end_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        return u'Вы не играете сейчас в игру'
    if storage.data[user_id]['state'] == 'game':
        storage.data[user_id]['state'] = 'waitForStart'
        return 'stop_game()'
    else:
        return u'Вы не играете сейчас в игру'


def c_change_article(session_continues, storage, user_id, username, article=''):
    if not session_continues:
        storage.new_user(username, user_id)
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return 'change_article(article)'
    if storage.data[user_id]['state'] == 'waitForStart':
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return 'change_article(article)'
    elif storage.data[user_id]['state'] == 'game':
        return u'Нельзя сменить целевую статью во время игры'
    else:
        return u'Ответьте на вопрос, плез'


def c_hitler_mode(session_continues, storage, user_id, username):
    c_change_article(session_continues, storage, user_id, username, 'Гитлер')


def c_score(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return 'get_score()'


def c_open(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    if not session_continues or not storage.data[user_id]['state'] == 'game':
        return 'Открыть статью можно только во время игры'
    else:
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return 'open_article()'


commands_list = {
    u'/help': c_help,
    '/start_game': c_start_game,
    '/end_game': c_end_game,
    '/change_article': c_change_article,
    '/hitler_mode': c_hitler_mode,
    '/score': c_score,
    '/open': c_open
}


# Модуль инициализации переменных
# -------------------------------------------------------------------------

def write_bot_name(bot):
    log_write('sys', bot.username + '\n', sys_time())


log_file = open('logs/logs.txt', 'a')

# bot = init_bot(settings.bot_token)

storage = Storage()
