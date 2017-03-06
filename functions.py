# coding: utf8

import sys
import time
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import urllib2

import settings
from settings import dictionary

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


def answer(bot, send_user_id, send_answer_text, reply_markup=None):
    if len(send_answer_text) == 0:
        return
    if isinstance(send_answer_text, unicode) or isinstance(send_answer_text, str):
        if reply_markup is None:
            result = bot.send_message(send_user_id, send_answer_text).wait()
        else:
            result = bot.send_message(send_user_id, send_answer_text, reply_markup=reply_markup).wait()
        log_write('bot', result, sys_time())
        # try:
        #     log_write('bot', send_answer_text, sys_time())
        # except Exception:
        #     pass
        return
    for answer_text in send_answer_text:
        if reply_markup is None:
            result = bot.send_message(send_user_id, answer_text).wait()
        else:
            result = bot.send_message(send_user_id, answer_text, reply_markup).wait()
        log_write('bot', result, sys_time())
        # try:
        #     log_write('bot', answer_text, sys_time())
        # except Exception:
        #     pass


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


def init_game(storage, user_id):
    link_to_open = settings.random_page_link
    links_list, current_article_url, header = open_link(link_to_open)
    answer_text = dictionary['this_is_links_list'] + str(header) + ':\n'
    for link in links_list:
        if link[0] > settings.max_links_count:
            break
        answer_text = answer_text + unicode(link[0]) + '. ' + link[1] + '\n'
    answer_text = answer_text + dictionary['your_goal_is'] + storage.data[user_id]['goal_article_header'] + dictionary['what_you_want_to_choose']

    storage.data[user_id]['state'] = 'game'
    storage.data[user_id]['question'] = 'answer_article_id'
    storage.data[user_id]['game'] = {
        'links_list': links_list,
        'current_article_url': current_article_url,
        'current_article_header': header,
        'links_count': 0
    }
    return answer_text


def change_article(storage, user_id, article_header, article_url, searching=False):
    if searching:
        new_links_list, current_article_url, header = open_link(article_url)
        if 'search' in current_article_url:
            answer_list = []  # Список собщений для отправки
            answer_text = u'Найденные статьи:\n'
            counter = 1
            for new_link in new_links_list:
                answer_text = answer_text + unicode(new_link[0]) + '. ' + new_link[1] + '\n'
                if counter >= settings.max_links_count:
                    answer_list.append(answer_text)
                    answer_text = ''
                    counter = 0
                counter += 1

            answer_text += u'\n\nВыберите нужную или наберите cancel для отмены'
            answer_list.append(answer_text)

            storage.data[user_id]['state'] = 'waitForCommandAnswer'
            storage.data[user_id]['question'] = 'answer_article_to_change_id'
            storage.data[user_id]['temp_data'] = new_links_list
            return answer_list
        else:
            article_header = header
            article_url = current_article_url

    if article_header is not None and article_url is not None:
        storage.data[user_id]['goal_article_header'] = article_header
        storage.data[user_id]['goal_article_url'] = article_url

        storage.data[user_id]['state'] = 'waitForStart'
        storage.data[user_id]['question'] = ''
        return dictionary['goal_article_was_changed'] + article_header
    elif article_url is not None:
        tmp1, tmp2, article_header = open_link(article_url)
        storage.data[user_id]['goal_article_header'] = article_header
        storage.data[user_id]['goal_article_url'] = article_url

        storage.data[user_id]['state'] = 'waitForStart'
        storage.data[user_id]['question'] = ''
        return dictionary['goal_article_was_changed'] + article_header
    else:
        storage.data[user_id]['question'] = 'article_link'

        return dictionary['enter_article_link']


def answer_article_id(storage, user_id, text):
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return dictionary['wrong_id']
    except IndexError:
        return dictionary['wrong_id']

    new_links_list, current_article_url, header = open_link(settings.url_prefix + link[2])
    storage.data[user_id]['game']['links_count'] += 1

    # Проверка, не дошли ли еще и не закончились ли ходы
    if header == storage.data[user_id]['goal_article_header']:
        result = dictionary['congratulations'] + str(storage.data[user_id]['game']['links_count']) + \
                 dictionary['steps']
        storage.del_user(user_id)
        return result

    if storage.data[user_id]['game']['links_count'] >= storage.data[user_id]['difficulty']:
        result = dictionary['no_more_steps'] + storage.data[user_id]['goal_article_header'] + \
                 dictionary['not_reached']
        storage.del_user(user_id)
        return result

    answer_list = []  # Список собщений для отправки
    answer_text = dictionary['this_is_links_list'] + str(link[1]) + ':\n'
    counter = 1
    for new_link in new_links_list:
        answer_text = answer_text + unicode(new_link[0]) + '. ' + new_link[1] + '\n'
        if counter >= settings.max_links_count:
            answer_list.append(answer_text)
            answer_text = ''
            counter = 0
        counter += 1

    answer_text += dictionary['your_goal_is'] + storage.data[user_id]['goal_article_header'] + \
              dictionary['steps_made'] + str(storage.data[user_id]['game']['links_count']) + \
              dictionary['what_you_want_to_choose']
    answer_list.append(answer_text)

    storage.data[user_id]['state'] = 'game'
    storage.data[user_id]['question'] = 'answer_article_id'
    storage.data[user_id]['game']['links_list'] = new_links_list
    storage.data[user_id]['game']['current_article_url'] = link[2]
    storage.data[user_id]['game']['current_article_header'] = link[1]

    return answer_list


def answer_article_to_change_id(storage, user_id, text):
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['temp_data']
        link = links_list[article_id - 1]
    except ValueError:
        return dictionary['wrong_id']
    except IndexError:
        return dictionary['wrong_id']

    new_links_list, current_article_url, header = open_link(settings.url_prefix + link[2])
    result = change_article(storage, user_id, header, settings.url_prefix + current_article_url)
    return result


def set_difficulty(storage, user_id):
    reply_markup = ReplyKeyboardMarkup.create(settings.keyboard, one_time_keyboard=True)

    storage.data[user_id]['state'] = 'waitForCommandAnswer'
    storage.data[user_id]['question'] = 'answer_difficulty'

    return dictionary['select_difficulty'], reply_markup


def answer_difficulty(storage, user_id, text):
    if text == u'Отмена':
        storage.data[user_id]['state'] = 'waitForStart'
        storage.data[user_id]['question'] = ''
        return dictionary['selecting_difficulty_canceled'], None
    try:
        storage.data[user_id]['difficulty'] = settings.difficulty_list[text]
        storage.data[user_id]['state'] = 'waitForStart'
        storage.data[user_id]['question'] = ''
        return dictionary['difficulty_was_changed'] + str(storage.data[user_id]['difficulty']), None
    except KeyError:
        reply_markup = ReplyKeyboardMarkup.create(settings.keyboard, one_time_keyboard=True)
        return dictionary['wrong_entered_difficulty'], reply_markup


# Модуль комманд бота
# -------------------------------------------------------------------------
# Порядок аргументов: session_continues, storage, user_id, username

def c_start(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return dictionary['hello_at_start'], None


def c_help(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return dictionary['commands_help'], None


def c_rules(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return dictionary['rules'][0] + \
           storage.data[user_id]['goal_article_header'] + \
           dictionary['rules'][1] +\
           unicode(storage.data[user_id]['difficulty']) + \
           dictionary['rules'][2], None


def c_start_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    if storage.data[user_id]['state'] == 'waitForStart':
        return init_game(storage, user_id), None
    elif storage.data[user_id]['state'] == 'game':
        return dictionary['game_already_started'], None
    else:
        return dictionary['give_answer'], None


def c_end_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        return dictionary['you_not_play'], None
    if storage.data[user_id]['state'] == 'game':
        storage.del_user(user_id)
        return dictionary['game_stopped'], None
    else:
        return dictionary['you_not_play'], None


def c_change_article(session_continues, storage, user_id, username, article_header=None, article_url=None):
    if not session_continues:
        storage.new_user(username, user_id)
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return change_article(storage, user_id, article_header, article_url), None
    if storage.data[user_id]['state'] == 'waitForStart':
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return change_article(storage, user_id, article_header, article_url), None
    elif storage.data[user_id]['state'] == 'game':
        return dictionary['cant_change_article_while_playing'], None
    else:
        return dictionary['give_answer'], None


def c_hitler_mode(session_continues, storage, user_id, username):
    result = c_change_article(session_continues, storage, user_id, username, settings.hitler_article_header,
                              settings.hitler_article_url)
    return result


def c_set_difficulty(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        result = set_difficulty(storage, user_id)
        return result
    if storage.data[user_id]['state'] == 'waitForStart':
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return set_difficulty(storage, user_id)
    elif storage.data[user_id]['state'] == 'game':
        return dictionary['cant_change_difficulty_while_playing'], None
    else:
        return dictionary['give_answer'], None


def c_score(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return 'get_score()', None


def c_open(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    if not session_continues or not storage.data[user_id]['state'] == 'game':
        return dictionary['opening_just_while_playing'], None
    else:
        storage.data[user_id]['state'] = 'waitForCommandAnswer'
        return 'open_article()', None


def understand_text(session_continues, storage, user_id, username, text):
    if not session_continues:
        storage.new_user(username, user_id)
        return dictionary['invite_to_start'], None
    if storage.data[user_id]['question'] == 'article_link':
        try:
            if 'http' in text:
                result = change_article(storage, user_id, None, text)
            else:
                result = change_article(storage, user_id, None, settings.search_template_prefix + text +
                                        settings.search_template_postfix, True)
            return result, None
        except ValueError:
            return dictionary['wrong_entered_url'], None
    elif storage.data[user_id]['question'] == 'answer_article_id':
        return answer_article_id(storage, user_id, text), None
    elif storage.data[user_id]['question'] == 'answer_article_to_change_id':
        storage.data[user_id]['state'] = 'waitForStart'
        storage.data[user_id]['question'] = ''
        if text == u'cancel':
            return u'Вы отменили выбор', None
        return answer_article_to_change_id(storage, user_id, text), None
    elif storage.data[user_id]['question'] == 'answer_difficulty':
        return answer_difficulty(storage, user_id, text)
    else:
        return dictionary['invite_to_start'], None


commands_list = {
    '/start': c_start,
    '/rules': c_rules,
    '/help': c_help,
    '/start_game': c_start_game,
    '/end_game': c_end_game,
    '/change_article': c_change_article,
    '/hitler_mode': c_hitler_mode,
    '/set_difficulty': c_set_difficulty,
    '/score': c_score,
    '/open': c_open
}


# Модуль инициализации переменных
# -------------------------------------------------------------------------

def write_bot_name(bot):
    log_write('sys', bot.username + '\n', sys_time())


log_file = open('logs/logs.txt', 'a')

# bot = init_bot(settings.bot_token)

# storage = Storage()
