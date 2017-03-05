# coding: utf8

import sys
import time
from twx.botapi import TelegramBot
from bs4 import BeautifulSoup
import urllib2

import settings
from storage import Storage

reload(sys)
sys.setdefaultencoding('utf8')


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
    try:
        log_write('bot', send_answer_text, sys_time())
    except Exception:
        pass


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
    print('Current Page is ' + str(current_page_header).decode('utf-8') + '\n')

    soup = soup.find(id="mw-content-text")
    a = soup.find_all('a')

    result = []
    link_id = 1
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
                    result.append([link_id, title, href])
                    link_id += 1
        except TypeError:
            log_write('sys', 'EMPTY HREF!!!', sys_time())  # Не происходит из-за проверки not (title is None)
    return result, current_page_link, current_page_header


def init_game(user_id):
    link_to_open = settings.random_page_link
    links_list, current_article_url, header = open_link(link_to_open)
    answer = u'Вот список ссылок по статье ' + str(header) + ':\n'
    for link in links_list:
        if link[0] > 100:
            break
        answer = answer + unicode(link[0]) + '. ' + link[1] + '\n'
    answer += u'\n(Вам нужно дойти до статьи\n' + storage.data[user_id]['goal_article_header'] + u')\n\nЧто выбираете?'

    storage.data[user_id]['state'] = 'game'
    storage.data[user_id]['question'] = 'answer_article_id'
    storage.data[user_id]['game'] = {
        'links_list': links_list,
        'current_article_url': current_article_url,
        'current_article_header': header,
        'links_count': 0
    }
    return answer


def change_article(user_id, article_header, article_url):
    # Лишнее условие?
    if article_header is not None and article_url is not None:
        storage.data[user_id]['goal_article_header'] = article_header
        storage.data[user_id]['goal_article_url'] = article_url
        return u'Целевая статья успешно изменена на ' + article_header
    elif article_url is not None:
        tmp1, tmp2, article_header = open_link(article_url)
        storage.data[user_id]['goal_article_header'] = article_header
        storage.data[user_id]['goal_article_url'] = article_url
        return u'Целевая статья успешно изменена на ' + article_header
    else:
        storage.data[user_id]['question'] = 'article_link'
        return u'Введите ссылку на статью'


def answer_article_id(storage, user_id, username, text):
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return 'Неверный номер'

    new_links_list, current_article_url, link[1] = open_link(settings.url_prefix + link[2])

    # Проверка, не дошли ли еще и не закончились ли ходы

    storage.data[user_id]['game']['links_count'] += 1
    answer = u'Вот список ссылок по статье ' + str(link[1]) + ':\n'
    for new_link in new_links_list:
        if new_link[0] > 100:
            break
        answer = answer + unicode(new_link[0]) + '. ' + new_link[1] + '\n'
    answer += u'\n(Вам нужно дойти до статьи\n' + storage.data[user_id]['goal_article_header'] + \
              u'\n\nУже сделано ходов: ' + str(storage.data[user_id]['game']['links_count']) + u')\n\nЧто выбираете?'

    storage.data[user_id]['state'] = 'game'
    storage.data[user_id]['question'] = 'answer_article_id'
    storage.data[user_id]['game']['links_list'] = new_links_list
    storage.data[user_id]['game']['current_article_url'] = link[2]
    storage.data[user_id]['game']['current_article_header'] = link[1]

    return answer


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
        return init_game(user_id)
    elif storage.data[user_id]['state'] == 'game':
        return u'Вы уже начали игру :)'
    else:
        return u'Ответьте на вопрос, плез'


def c_end_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        return u'Вы не играете сейчас в игру'
    if storage.data[user_id]['state'] == 'game':
        storage.del_user(user_id)
        return 'stop_game()'
    else:
        return u'Вы не играете сейчас в игру'


def c_change_article(session_continues, storage, user_id, username, article_header=None, article_url=None):
    if not session_continues:
        storage.new_user(username, user_id)
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return change_article(user_id, article_header, article_url)
    if storage.data[user_id]['state'] == 'waitForStart':
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return change_article(user_id, article_header, article_url)
    elif storage.data[user_id]['state'] == 'game':
        return u'Нельзя сменить целевую статью во время игры'
    else:
        return u'Ответьте на вопрос, плез'


def c_hitler_mode(session_continues, storage, user_id, username):
    result = c_change_article(session_continues, storage, user_id, username, settings.hitler_article_header,
                              settings.hitler_article_url)
    storage.data[user_id]['state'] = 'waitForStart'
    storage.data[user_id]['question'] = ''
    return result


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


def understand_text(session_continues, storage, user_id, username, text):
    if not session_continues:
        storage.new_user(username, user_id)
        return u'Хотите начать игру?\nНаберите /start_game или посмотрите /help для справки по командам'
    if storage.data[user_id]['question'] == 'article_link':
        try:
            result = change_article(user_id, None, text)
            storage.data[user_id]['state'] = 'waitForStart'
            storage.data[user_id]['question'] = ''
            return result
        except ValueError:
            return u'Ссылка не работает, попробуйте снова'
    elif storage.data[user_id]['question'] == 'answer_article_id':
        return answer_article_id(storage, user_id, username, text)
    else:
        return u'Хотите начать игру?\nНаберите /start_game или посмотрите /help для справки по командам'


commands_list = {
    '/help': c_help,
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
