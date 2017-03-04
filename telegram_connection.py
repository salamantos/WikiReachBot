# coding=utf-8
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
from log_writer import log_write, sys_time


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
    new_bot = TelegramBot(init_token)
    new_bot.update_bot_info().wait()
    return new_bot


# answer(281389974, 'Ты пидор!')
