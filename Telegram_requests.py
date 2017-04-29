# coding=utf-8
import settings
from settings import FatalError, EasyError
from logs import *
from twx.botapi import TelegramBot, Error

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль запросов к Телеграму
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Получаем данные из обновления
def extract_update_info(update_object):
    error = ''
    try:
        if update_object.edited_message is not None:
            error += 'Edited message'
        elif update_object.message is None:
            error += 'None message'
        elif update_object.message.new_chat_member is not None \
                or update_object.message.left_chat_member is not None:
            error += 'User join/left'
    except AttributeError:
        error += 'AttributeError in extract_update_info'

    if error != '':
        raise EasyError('extract_update_info error: {}'.format(error))

    # try AttributeError
    update_id = update_object.update_id
    received_user_id = update_object.message.sender.id
    received_username = update_object.message.sender.username
    chat_id = update_object.message.chat.id
    # chat_type = update_object.message.chat.type  # Пока работаем с приватным, проверить
    request_date = update_object.message.date
    received_text = update_object.message.text

    return update_id, received_user_id, chat_id, received_username, received_text, \
        request_date


# Пытаемся отправить сообщение из очереди
def send_answer_from_queue(log_file, storage, bot, send_user_id, chat_id, send_answer_text,
                           reply_markup):
    if reply_markup is None:
        result = bot.send_message(chat_id, send_answer_text).wait()
        # print 1
        log_write(log_file, 'bot', result)
    else:
        result = bot.send_message(chat_id, send_answer_text, reply_markup=reply_markup).wait()
        # print 2
        log_write(log_file, 'bot', result)
    storage.modify_local_storage(send_user_id,
                                          last_message_sent=sys_time()
                                          )
    if isinstance(result, Error):
        # Пытаемся снова через больший промежуток времени
        storage.modify_local_storage(
            send_user_id,
            last_message_sent=sys_time() + settings.BIG_TIMEOUT_PERSONAL_MESSAGES
        )
        # print 5
        return False

    return True


# Отвечает за отправку и временное хранение сообщений
def answer(log_file, storage, bot, send_user_id, chat_id, send_answer_text, reply_markup=None,
           del_msg=False):
    # С пустой строкой ответа просто отправляет данные из очереди
    class Queue:
        def __init__(self):
            self.items = []

        def is_empty(self):
            return self.items == []

        def enqueue(self, item):
            self.items.insert(0, item)

        def dequeue(self):
            return self.items.pop()

        def size(self):
            return len(self.items)

    error = ''

    # При первом вызове функции заводим очередь
    try:
        answer.queue.is_empty()
    except AttributeError:
        answer.queue = Queue()

    # Удаляем из очереди все предыдущие неотправленные сообщения этому пользователю
    if del_msg and len(send_answer_text) != 0:
        temp_queue = Queue()
        try:
            while not answer.queue.is_empty():
                send_user_id_from_queue1, chat_id1, send_answer_text1, reply_markup1 = \
                    answer.queue.dequeue()
                if send_user_id != send_user_id_from_queue1:
                    temp_queue.enqueue(
                        (send_user_id_from_queue1, chat_id1, send_answer_text1, reply_markup1))

            while not temp_queue.is_empty():
                answer.queue.enqueue((temp_queue.dequeue()))
        except KeyError:
            error += 'KeyError'

    # Добавляем сообщения в очередь
    if len(send_answer_text) != 0:
        # Если строка
        if isinstance(send_answer_text, unicode) or isinstance(send_answer_text, str):
            answer.queue.enqueue((send_user_id, chat_id, send_answer_text, reply_markup))
        # Иначе, если список строк
        else:
            for answer_text in send_answer_text:
                answer.queue.enqueue((send_user_id, chat_id, answer_text, reply_markup))

    temp_queue = Queue()
    users_skip_list = []  # Пользователи, которым пока не отправляем сообщние
    try:
        while not answer.queue.is_empty():
            send_user_id, chat_id, send_answer_text, reply_markup = answer.queue.dequeue()
            if (sys_time() - storage.data[send_user_id]['last_message_sent'] >
                    settings.TIMEOUT_PERSONAL_MESSAGES) and send_user_id not in users_skip_list:
                error_get, success = send_answer_from_queue(log_file, storage, bot, send_user_id,
                                                            chat_id, send_answer_text,
                                                            reply_markup)
                error += error_get
                if success:
                    continue
            if send_user_id not in users_skip_list:
                users_skip_list.append(send_user_id)
            temp_queue.enqueue((send_user_id, chat_id, send_answer_text, reply_markup))

        while not temp_queue.is_empty():
            answer.queue.enqueue((temp_queue.dequeue()))
    except KeyError:
        error += 'KeyError'

    raise FatalError('Error in answer function: {}'.format(error))


# Инициализация бота
def init_bot(init_token):
    bot = TelegramBot(init_token)
    bot.update_bot_info().wait()
    return bot


# Вывод в логи имени бота
def write_bot_name(log_file, bot):
    try:
        log_write(log_file, 'sys', '{}\n'.format(bot.username))
    except TypeError:
        raise FatalError('No internet connection')


# Получение обновлений с сервера Телеграма
def get_updates_for_bot(bot, offset):
    result = bot.get_updates(offset).wait()
    if result is None:
        result = []
    return result
