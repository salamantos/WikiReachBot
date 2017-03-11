# coding=utf-8

import time
import re
from functions import sys_time, log_write, write_bot_name, extract_update_info, get_updates_for_bot, commands_list, \
    answer, log_file, init_bot, understand_text
from storage import Storage
import settings
from settings import dictionary

# Включение бота
reset_messages = raw_input('Reset messages? y/n\n')
if reset_messages == 'y':
    reset_messages = True
else:
    reset_messages = False
log_write('sys', '------------- Начало сеанса -------------', sys_time())
bot = init_bot(settings.bot_token)
error = write_bot_name(bot)
if not error:
    print 'successfully'
else:
    print error
    exit(0)
storage = Storage()
offset = 0

# Пропускаем пропущенные сообщения и выводим сообщение об этом пользователям
if reset_messages:
    updates = get_updates_for_bot(bot, offset)
    if updates:
        reset_file = open('logs/reset_file.txt', 'a')
        reset_file.write(str(updates))
        reset_file.close()
        offset = updates[-1].update_id + 1

# log_file.close()  # Fix it!

if not error:
    print 'successfully'
else:
    print error

# Запуск прослушки Телеграма

# error = ''
try:
    answer_text = u'<Заготовка под ответ>'
    reply_markup = None
    while True:
        updates = get_updates_for_bot(bot, offset)  # Если нет обновлений, вернет пустой список
        for update in updates:
            # Получаем информацию о сообщении
            error, offset, user_id, chat_id, username, text, message_date = extract_update_info(update)
            if error != '':
                offset += 1
                print error
                continue
            give_answer = False  # Готов ли ответ

            # Если не текстовое сообщение
            if text is None:
                text = u'(Нет текста)'
                answer_text = dictionary['no_text']
                give_answer = True

            # Логи
            try:
                log_write('usr', update, message_date, username, user_id)
                log_write('usr', text.encode('utf-8'), message_date, username, user_id)
            except UnicodeError:
                log_write('usr', 'UnicodeError', message_date, username, user_id)

            # Если получили комманду
            if text[0] == '/' and not give_answer:
                try:
                    if '@WikiReachBot' in text:
                        text = re.sub(r'@WikiReachBot', '', text)
                    if '/answer' in text:
                        text = re.sub(r'/answer ', '', text)
                        error, answer_text, reply_markup = commands_list['/answer'](user_id in storage.data, storage,
                                                                                    user_id, username, text)
                        give_answer = True

                    if not give_answer:
                        error, answer_text, reply_markup = commands_list.get(text)(user_id in storage.data, storage,
                                                                                   user_id, username)

                except TypeError:
                    answer_text = dictionary['non_existent_command']
                give_answer = True

            # Если текстовый запрос, пытаемся понять его
            if not give_answer:
                error, answer_text, reply_markup = understand_text(user_id in storage.data, storage,
                                                                   user_id, username, text)
                give_answer = True

            if error == '' or error == 'Wrong url':
                answer(bot, chat_id, answer_text, reply_markup)
            else:
                print "err: "
                print error

            offset += 1  # id следующего обновления
        time.sleep(0.01)

except KeyboardInterrupt:
    log_write('endl', '', sys_time())
    log_write('sys', 'Бот остановлен.', sys_time())
# except:
#     log_write('Неизвестная ошибка')
finally:
    log_write('sys', '------------- Конец сеанса --------------\n\n\n', sys_time())
    log_file.close()  # Fix it!
