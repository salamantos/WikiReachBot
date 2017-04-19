# coding: utf8

from Wiki_requests import *
from twx.botapi import ReplyKeyboardMarkup
from settings import *

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль комманд бота
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Формируем ответ из полученного списка ссылок
def form_answer_from_links_list(answer_text, new_links_list, postfix_answer_text):
    answer_list = []  # Список собщений для отправки
    counter = 1
    for new_link in new_links_list:
        answer_text = '{0}{1}. {2}\n'.format(answer_text, unicode(new_link[0]), new_link[1])
        if counter >= MAX_LINKS_COUNT:
            answer_list.append(answer_text)
            answer_text = ''
            counter = 0
        counter += 1

    answer_text += postfix_answer_text
    answer_list.append(answer_text)
    return answer_list


# Начало игры
def init_game(storage, user_id):
    error = ''
    link_to_open = RANDOM_PAGE_LINK
    error_get, links_list, current_article_url, header = open_url(link_to_open)
    error += error_get

    answer_list = form_answer_from_links_list(
        '{0}{1}:\n'.format(THIS_IS_LINKS_LIST, header), links_list,
        '{0}{1})\n\n{2}'.format(YOUR_GOAL_IS, storage.data[user_id]['goal_article_header'],
                                WHAT_YOU_WANT_TO_CHOOSE))

    error += storage.modify_local_storage(user_id,
                                          state='game',
                                          question='answer_article_id',
                                          game={
                                              'links_list': links_list,
                                              'current_article_url': current_article_url,
                                              'current_article_header': header,
                                              'links_count': 0,
                                              'links_available': 1000000
                                          })
    return error, answer_list


def form_messages(storage, user_id, case, link=None):
    sent_links_count = 0  # Число отправленных ссылок
    answer_list = []  # Список собщений для отправки
    links_list = storage.data[user_id]['game']['links_list']
    if case == 'more_links':
        answer_text = MORE_LINKS
        counter_start = storage.data[user_id]['game']['links_available']
        counter_end = counter_start + MAX_LINKS_COUNT * SPLIT_MESSAGES_COUNT
    else:
        answer_text = '{0}{1}:\n'.format(THIS_IS_LINKS_LIST, link[1])
        counter_start = 0
        counter_end = len(links_list)
    if case == 'part_of_links':
        counter_end = MAX_LINKS_COUNT * SPLIT_MESSAGES_COUNT

    counter = 1
    i = counter_start
    no_more_links = False
    while i < counter_end:
        add_text = '{0}. {1}\n'.format(unicode(links_list[i][0]), links_list[i][1])
        if len(answer_text) + len(add_text) > MAX_MESSAGE_SIZE:
            answer_list.append(answer_text)
            answer_text = ''
            counter = 0
        else:
            answer_text += add_text
            if counter >= MAX_LINKS_COUNT and links_list[i][0] != counter_start + \
                    MAX_LINKS_COUNT * SPLIT_MESSAGES_COUNT:
                answer_list.append(answer_text)
                answer_text = ''
                counter = 0
            i += 1
        counter += 1
        sent_links_count = i
        # Если ссылки закончились
        if i == len(links_list) and case == 'more_links':
            storage.data[user_id]['game']['links_available'] = 1000000
            answer_text = '{0}\n{1}'.format(answer_text, WHAT_YOU_WANT_TO_CHOOSE)
            no_more_links = True
            break
    sent_links_count -= counter_start
    if not no_more_links and case == 'more_links':
        answer_text += '\n{0}'.format(CHOOSE_OR_NEED_MORE)
    if case == 'all_links':
        answer_text += '{0}{1}{2}{3})\n\n{4}'.format(
            YOUR_GOAL_IS, storage.data[user_id]['goal_article_header'],
            STEPS_MADE, storage.data[user_id]['game']['links_count'], WHAT_YOU_WANT_TO_CHOOSE)
    if case == 'part_of_links':
        answer_text += '{0}{1}{2}{3})\n\n{4}'.format(
            YOUR_GOAL_IS, storage.data[user_id]['goal_article_header'], STEPS_MADE,
            storage.data[user_id]['game']['links_count'], CHOOSE_OR_NEED_MORE)
    answer_list.append(answer_text)
    return sent_links_count, answer_list


# Вызывается при переходе на другую статью во время игры
def answer_article_id(storage, user_id, text):
    error = ''
    if text == u'more':
        if storage.data[user_id]['game']['links_available'] != 1000000:
            # Формируем сообщения
            sent_links_count, answer_list = form_messages(storage, user_id, 'more_links')
            storage.data[user_id]['game']['links_available'] += sent_links_count
            return '', answer_list
        else:
            return '', WRONG_ID
    if int(text) < 0:
        return '', WRONG_ID
    try:
        article_id = int(text)
        if article_id > storage.data[user_id]['game']['links_available']:
            return '', WRONG_ID
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return '', WRONG_ID
    except IndexError:
        return '', WRONG_ID

    error_get, new_links_list, current_article_url, header = open_url(
        URL_PREFIX + link[2])
    error += error_get
    storage.data[user_id]['game']['links_count'] += 1

    # Проверка, не дошли ли еще и не закончились ли ходы
    if header == storage.data[user_id]['goal_article_header']:
        result = '{0}{1}{2}'.format(
            CONGRATULATIONS, storage.data[user_id]['game']['links_count'], STEPS)
        error += storage.db_sync_upload(user_id, games_won=True)
        storage.del_user(user_id)
        return error, result

    if storage.data[user_id]['game']['links_count'] >= storage.data[user_id]['difficulty']:
        result = '{0}{1}{2}'.format(
            NO_MORE_STEPS, storage.data[user_id]['goal_article_header'], NOT_REACHED)
        error += storage.db_sync_upload(user_id, games_won=False)
        storage.del_user(user_id)
        return error, result

    # Проверка, не попали ли на статью, где нет ссылок
    if len(new_links_list) == 0:
        result = NO_LINKS_IN_CHOSEN_ARTICLE
        error += storage.db_sync_upload(user_id, games_won=False)
        storage.del_user(user_id)
        return error, result

    storage.data[user_id]['game']['links_list'] = new_links_list
    storage.data[user_id]['game']['current_article_url'] = link[2]
    storage.data[user_id]['game']['current_article_header'] = link[1]

    if len(new_links_list) < MAX_LINKS_COUNT * MAX_MESSAGES_COUNT:
        sent_links_count, answer_list = form_messages(storage, user_id, 'all_links', link)
        storage.data[user_id]['game']['links_available'] = 1000000
    else:
        sent_links_count, answer_list = form_messages(storage, user_id, 'part_of_links', link)
        storage.data[user_id]['game']['links_available'] = sent_links_count
        pass

    return error, answer_list


# Вызывается при наборе команды смены статьи
def change_article(storage, user_id, article_header, article_url, searching=False):
    error = ''
    # Если нужен поис по Википедии
    if searching:
        error_get, new_links_list, current_article_url, header = open_url(article_url)
        error += error_get
        if error != '':
            error += 'Wrong url'
            return error, 'Wrong url'

        if 'search' in current_article_url:
            answer_list = form_answer_from_links_list(ARTICLES_FOUND, new_links_list,
                                                      SELECT_ARTICLE_OR_CANCEL)

            error += storage.modify_local_storage(user_id,
                                                  state='waitForCommandAnswer',
                                                  question='answer_article_to_change_id',
                                                  temp_data=new_links_list
                                                  )
            return error, answer_list
        else:
            article_header = header
            article_url = current_article_url

    # Если известна вся информация о статье
    if article_header is not None and article_url is not None:
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question='',
                                              goal_article_header=article_header,
                                              goal_article_url=article_url
                                              )
        return error, GOAL_ARTICLE_WAS_CHANGED + article_header
    elif article_url is not None:
        error_get, tmp1, tmp2, article_header = open_url(article_url)
        error += error_get
        if error != '':
            error += 'Wrong url'
            return error, 'Wrong url'

        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question='',
                                              goal_article_header=article_header,
                                              goal_article_url=article_url
                                              )
        return error, GOAL_ARTICLE_WAS_CHANGED + article_header
    else:
        error += storage.modify_local_storage(user_id,
                                              question='article_link',
                                              )
        return error, ENTER_ARTICLE_LINK


# Вызывается при выборе статьи из предложенного результата поиска
def answer_article_to_change_id(storage, user_id, text):
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['temp_data']
        link = links_list[article_id - 1]
    except ValueError:
        return '', WRONG_ID
    except IndexError:
        return '', WRONG_ID

    new_links_list, current_article_url, header = open_url(URL_PREFIX + link[2])
    result = change_article(storage, user_id, header, URL_PREFIX + current_article_url)
    return '', result


# Смена сложности игры
def set_difficulty(storage, user_id):
    reply_markup = ReplyKeyboardMarkup.create(KEYBOARD, one_time_keyboard=True)

    storage.modify_local_storage(user_id,
                                 state='waitForCommandAnswer',
                                 question='answer_difficulty'
                                 )

    return '', SELECT_DIFFICULTY, reply_markup


# Ответ на запрос о смене сложности
def answer_difficulty(storage, user_id, text):
    error = ''
    if text == u'Отмена':
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question=''
                                              )
        return error, SELECTING_DIFFICULTY_CANCELED, None
    try:
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question='',
                                              difficulty=DIFFICULTY_LIST[text]
                                              )
        return error, DIFFICULTY_WAS_CHANGED + str(
            storage.data[user_id]['difficulty']), None
    except KeyError:
        reply_markup = ReplyKeyboardMarkup.create(KEYBOARD, one_time_keyboard=True)
        return error, WRONG_ENTERED_DIFFICULTY, reply_markup


# Выдает ссылку на статью
def open_link_by_id(storage, user_id, text):
    error = ''
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return '', WRONG_ID
    except IndexError:
        return '', WRONG_ID

    error += storage.modify_local_storage(user_id,
                                          question='answer_article_id'
                                          )
    answer_text = [URL_PREFIX + link[2], u'Теперь продолжим, что вы выбираете?))']

    return '', answer_text


# Показывает счет (статистику)
def get_score(storage, user_id):
    return '', storage.data[user_id]['games_count'], storage.data[user_id]['games_won']


# Парсинг комманд
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def c_start(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', HELLO_AT_START, None


def c_help(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', COMMANDS_HELP, None


def c_rules(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', '{0}{1}{2}{3}{4}'.format(
        RULES[0], storage.data[user_id]['goal_article_header'], RULES[1],
        unicode(storage.data[user_id]['difficulty']), RULES[2]), None


def c_start_game(session_continues, storage, user_id, username):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] == 'waitForStart':
        error_get, answer_text = init_game(storage, user_id)
        error += error_get
        return error, answer_text, None
    elif storage.data[user_id]['state'] == 'game':
        return '', GAME_ALREADY_STARTED, None
    else:
        return '', GIVE_ANSWER, None


def c_end_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        return '', YOU_NOT_PLAY, None

    if storage.data[user_id]['state'] == 'game':
        storage.del_user(user_id)
        error = storage.db_sync_upload(user_id, games_won=False)
        return error, GAME_STOPPED, None
    else:
        return '', YOU_NOT_PLAY, None


def c_change_article(session_continues, storage, user_id, username, article_header=None,
                     article_url=None):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] == 'waitForStart':
        error += storage.modify_local_storage(user_id,
                                              state='waitForCommandAnswer'
                                              )
        error_get, answer_text = change_article(storage, user_id, article_header, article_url)
        error += error_get
        return error, answer_text, None
    elif storage.data[user_id]['state'] == 'game':
        return '', CANT_CHANGE_DIFFICULTY_WHILE_PLAYING, None
    else:
        return '', GIVE_ANSWER, None


def c_hitler_mode(session_continues, storage, user_id, username):
    result = c_change_article(session_continues, storage, user_id, username,
                              HITLER_ARTICLE_HEADER,
                              HITLER_ARTICLE_URL)
    return result


def c_set_difficulty(session_continues, storage, user_id, username):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] == 'waitForStart':
        error += storage.modify_local_storage(user_id,
                                              state='waitForCommandAnswer'
                                              )
        error_get, answer_text, reply_markup = set_difficulty(storage, user_id)
        error += error_get
        return error, answer_text, reply_markup
    elif storage.data[user_id]['state'] == 'game':
        return error, CANT_CHANGE_DIFFICULTY_WHILE_PLAYING, None
    else:
        return error, GIVE_ANSWER, None


def c_score(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    error, games_count, games_won = get_score(storage, user_id)

    return error, '{0}{1}{2}{3}{4}'.format(
        SCORE1, unicode(games_count), SCORE2, unicode(games_won), SCORE3), None


def c_open(session_continues, storage, user_id, username):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] != 'game':
        return '', OPENING_JUST_WHILE_PLAYING, None
    else:
        error += storage.modify_local_storage(user_id,
                                              state='waitForCommandAnswer',
                                              question='answer_opening_article_id'
                                              )
        return error, OPEN_TO_GET_LINK, None


def c_answer(session_continues, storage, user_id, username, text):
    error = ''
    error_get, answer_text, reply_markup = understand_text(session_continues, storage, user_id,
                                                           username, text)
    error += error_get
    return error, answer_text, reply_markup


def understand_text(session_continues, storage, user_id, username, text):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)
        return error, INVITE_TO_START, None

    if storage.data[user_id]['question'] == 'article_link':
        try:
            if 'http' in text:
                error_get, answer_text = change_article(storage, user_id, None, text)
                error += error_get
            else:
                error_get, answer_text = change_article(storage, user_id, None,
                                                        SEARCH_TEMPLATE_PREFIX + text +
                                                        SEARCH_TEMPLATE_POSTFIX, True)
                error += error_get
            return error, answer_text, None
        except ValueError:
            return error, WRONG_ENTERED_URL, None
    elif storage.data[user_id]['question'] == 'answer_article_id':
        error_get, answer_text = answer_article_id(storage, user_id, text)
        error += error_get
        return error, answer_text, None
    elif storage.data[user_id]['question'] == 'answer_article_to_change_id':
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question=''
                                              )
        if text == u'cancel':
            return error, YOU_CANCELED_ARTICLE, None
        error_get, answer_text = answer_article_to_change_id(storage, user_id, text)
        error += error_get
        return error, answer_text, None
    elif storage.data[user_id]['question'] == 'answer_difficulty':
        return answer_difficulty(storage, user_id, text)
    elif storage.data[user_id]['question'] == 'answer_opening_article_id':
        error_get, answer_text = open_link_by_id(storage, user_id, text)
        error += error_get
        return error, answer_text, None
    else:
        return error, INVITE_TO_START, None


commands_list = {
    '/start': c_start,
    '/rules': c_rules,
    '/help': c_help,
    '/start_game': c_start_game,
    '/end_game': c_end_game,
    '/answer': c_answer,
    '/change_article': c_change_article,
    '/hitler_mode': c_hitler_mode,
    '/set_difficulty': c_set_difficulty,
    '/score': c_score,
    '/open': c_open
}
