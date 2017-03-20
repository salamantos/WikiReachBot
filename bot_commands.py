# coding: utf8

from Wiki_requests import *
from twx.botapi import ReplyKeyboardMarkup
from settings import dictionary

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль комманд бота
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def form_answer_from_links_list(answer_text, new_links_list, postfix_answer_text):
    answer_list = []  # Список собщений для отправки
    counter = 1
    for new_link in new_links_list:
        answer_text = answer_text + unicode(new_link[0]) + '. ' + new_link[1] + '\n'
        if counter >= settings.max_links_count:
            answer_list.append(answer_text)
            answer_text = ''
            counter = 0
        counter += 1

    answer_text += postfix_answer_text
    answer_list.append(answer_text)
    return answer_list


def init_game(storage, user_id):
    error = ''
    link_to_open = settings.random_page_link
    error_get, links_list, current_article_url, header = open_url(link_to_open)
    error += error_get
    # if error != '':
    #     error += 'Wrong url'
    #     return error, 'Wrong url'

    answer_list = form_answer_from_links_list(dictionary['this_is_links_list'] + str(header) + ':\n', links_list,
                                              dictionary['your_goal_is'] + storage.data[user_id][
                                                  'goal_article_header'] + dictionary['what_you_want_to_choose'])

    error += storage.modify_local_storage(user_id,
                                          state='game',
                                          question='answer_article_id',
                                          game={
                                              'links_list': links_list,
                                              'current_article_url': current_article_url,
                                              'current_article_header': header,
                                              'links_count': 0
                                          })
    return error, answer_list


def change_article(storage, user_id, article_header, article_url, searching=False):
    error = ''
    if searching:
        error_get, new_links_list, current_article_url, header = open_url(article_url)
        error += error_get
        if error != '':
            error += 'Wrong url'
            return error, 'Wrong url'

        if 'search' in current_article_url:
            answer_list = form_answer_from_links_list(u'Найденные статьи:\n', new_links_list,
                                                      u'\nВыберите нужную или наберите cancel для отмены')

            error += storage.modify_local_storage(user_id,
                                                  state='waitForCommandAnswer',
                                                  question='answer_article_to_change_id',
                                                  temp_data=new_links_list
                                                  )
            return error, answer_list
        else:
            article_header = header
            article_url = current_article_url

    if article_header is not None and article_url is not None:
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question='',
                                              goal_article_header=article_header,
                                              goal_article_url=article_url
                                              )
        return error, dictionary['goal_article_was_changed'] + article_header
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
        return error, dictionary['goal_article_was_changed'] + article_header
    else:
        error += storage.modify_local_storage(user_id,
                                              question='article_link',
                                              )
        return error, dictionary['enter_article_link']


def answer_article_id(storage, user_id, text):
    error = ''
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return '', dictionary['wrong_id']
    except IndexError:
        return '', dictionary['wrong_id']

    error_get, new_links_list, current_article_url, header = open_url(settings.url_prefix + link[2])
    error += error_get
    storage.data[user_id]['game']['links_count'] += 1
    error += storage.modify_local_storage(user_id,
                                          game=storage.data[user_id]['game'],
                                          )

    # Проверка, не дошли ли еще и не закончились ли ходы
    if header == storage.data[user_id]['goal_article_header']:
        result = dictionary['congratulations'] + str(storage.data[user_id]['game']['links_count']) + \
                 dictionary['steps']
        error += storage.db_sync_upload(user_id, games_won=True)
        storage.del_user(user_id)
        return error, result

    if storage.data[user_id]['game']['links_count'] >= storage.data[user_id]['difficulty']:
        result = dictionary['no_more_steps'] + storage.data[user_id]['goal_article_header'] + \
                 dictionary['not_reached']
        error += storage.db_sync_upload(user_id, games_won=False)
        storage.del_user(user_id)
        return error, result

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

    storage.data[user_id]['game']['links_list'] = new_links_list
    storage.data[user_id]['game']['current_article_url'] = link[2]
    storage.data[user_id]['game']['current_article_header'] = link[1]
    error += storage.modify_local_storage(user_id,
                                          state='game',
                                          question='answer_article_id',
                                          game=storage.data[user_id]['game']
                                          )

    return error, answer_list


def answer_article_to_change_id(storage, user_id, text):
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['temp_data']
        link = links_list[article_id - 1]
    except ValueError:
        return '', dictionary['wrong_id']
    except IndexError:
        return '', dictionary['wrong_id']

    new_links_list, current_article_url, header = open_url(settings.url_prefix + link[2])
    result = change_article(storage, user_id, header, settings.url_prefix + current_article_url)
    return '', result


def set_difficulty(storage, user_id):
    reply_markup = ReplyKeyboardMarkup.create(settings.keyboard, one_time_keyboard=True)

    storage.modify_local_storage(user_id,
                                 state='waitForCommandAnswer',
                                 question='answer_difficulty'
                                 )

    return '', dictionary['select_difficulty'], reply_markup


def answer_difficulty(storage, user_id, text):
    error = ''
    if text == u'Отмена':
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question=''
                                              )
        return error, dictionary['selecting_difficulty_canceled'], None
    try:
        error += storage.modify_local_storage(user_id,
                                              state='waitForStart',
                                              question='',
                                              difficulty=settings.difficulty_list[text]
                                              )
        return error, dictionary['difficulty_was_changed'] + str(storage.data[user_id]['difficulty']), None
    except KeyError:
        reply_markup = ReplyKeyboardMarkup.create(settings.keyboard, one_time_keyboard=True)
        return error, dictionary['wrong_entered_difficulty'], reply_markup


def open_link_by_id(storage, user_id, text):
    error = ''
    try:
        article_id = int(text)
        links_list = storage.data[user_id]['game']['links_list']
        link = links_list[article_id - 1]
    except ValueError:
        return '', dictionary['wrong_id']
    except IndexError:
        return '', dictionary['wrong_id']

    error += storage.modify_local_storage(user_id,
                                          question='answer_article_id'
                                          )
    answer_text = [settings.url_prefix + link[2], u'Теперь продолжим, что вы выбираете?))']

    return '', answer_text


def get_score(storage, user_id):
    return '', storage.data[user_id]['games_count'], storage.data[user_id]['games_won']


# Парсинг комманд
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def c_start(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', dictionary['hello_at_start'], None


def c_help(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', dictionary['commands_help'], None


def c_rules(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    return '', dictionary['rules'][0] + \
           storage.data[user_id]['goal_article_header'] + \
           dictionary['rules'][1] + \
           unicode(storage.data[user_id]['difficulty']) + \
           dictionary['rules'][2], None


def c_start_game(session_continues, storage, user_id, username):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] == 'waitForStart':
        error_get, answer_text = init_game(storage, user_id)
        error += error_get
        return error, answer_text, None
    elif storage.data[user_id]['state'] == 'game':
        return '', dictionary['game_already_started'], None
    else:
        return '', dictionary['give_answer'], None


def c_end_game(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
        return '', dictionary['you_not_play'], None

    if storage.data[user_id]['state'] == 'game':
        storage.del_user(user_id)
        error = storage.db_sync_upload(user_id, games_won=False)
        return error, dictionary['game_stopped'], None
    else:
        return '', dictionary['you_not_play'], None


def c_change_article(session_continues, storage, user_id, username, article_header=None, article_url=None):
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
        return '', dictionary['cant_change_article_while_playing'], None
    else:
        return '', dictionary['give_answer'], None


def c_hitler_mode(session_continues, storage, user_id, username):
    result = c_change_article(session_continues, storage, user_id, username, settings.hitler_article_header,
                              settings.hitler_article_url)
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
        return error, dictionary['cant_change_difficulty_while_playing'], None
    else:
        return error, dictionary['give_answer'], None


def c_score(session_continues, storage, user_id, username):
    if not session_continues:
        storage.new_user(username, user_id)
    error, games_count, games_won = get_score(storage, user_id)

    return error, u'Игр сыграно: ' + unicode(games_count) + u'\nВы победили в ' + unicode(games_won) + u' из них', None


def c_open(session_continues, storage, user_id, username):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)

    if storage.data[user_id]['state'] != 'game':
        return '', dictionary['opening_just_while_playing'], None
    else:
        error += storage.modify_local_storage(user_id,
                                              state='waitForCommandAnswer',
                                              question='answer_opening_article_id'
                                              )
        return error, u'Введите номер статьи из списка', None


def c_answer(session_continues, storage, user_id, username, text):
    error = ''
    error_get, answer_text, reply_markup = understand_text(session_continues, storage, user_id, username, text)
    error += error_get
    return error, answer_text, reply_markup


def understand_text(session_continues, storage, user_id, username, text):
    error = ''
    if not session_continues:
        storage.new_user(username, user_id)
        return error, dictionary['invite_to_start'], None

    if storage.data[user_id]['question'] == 'article_link':
        try:
            if 'http' in text:
                error_get, answer_text = change_article(storage, user_id, None, text)
                error += error_get
            else:
                error_get, answer_text = change_article(storage, user_id, None, settings.search_template_prefix + text +
                                                        settings.search_template_postfix, True)
                error += error_get
            return error, answer_text, None
        except ValueError:
            return error, dictionary['wrong_entered_url'], None
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
            return error, u'Вы отменили выбор', None
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
        return error, dictionary['invite_to_start'], None


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
