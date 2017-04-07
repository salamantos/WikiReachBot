# coding=utf-8

import re
from bot_commands import commands_list, understand_text
from storage import Storage
from settings import dictionary
from Telegram_requests import *

# Включение бота
reset_messages = raw_input('Reset messages? y/n\n')
if reset_messages == 'y':
    reset_messages = True
else:
    reset_messages = False

log_file = open('logs/logs.txt', 'a')
log_write(log_file, 'sys', '------------- Начало сеанса -------------', sys_time())
bot = init_bot(settings.bot_token)
error = write_bot_name(log_file, bot)
if not error:
    print 'successfully'
else:
    print error
    exit(0)
storage = Storage()
offset = 0

# Пропускаем пропущенные сообщения
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
    error = ''

# Запуск прослушки Телеграма
try:
    answer_text = u'<Заготовка под ответ>'
    reply_markup = None
    while True:
        updates = get_updates_for_bot(bot, offset)  # Если нет обновлений, вернет пустой список
        for update in updates:
            # Получаем информацию о сообщении
            error_get, offset, user_id, chat_id, username, text, \
                message_date = extract_update_info(update)
            error += error_get
            if error != '':
                offset += 1
                print error
                error = ''
                continue
            give_answer = False  # Готов ли ответ

            # Если не текстовое сообщение
            if text is None:
                text = u'(Нет текста)'
                answer_text = dictionary['no_text']
                give_answer = True

            # Логи
            try:
                log_write(log_file, 'usr', update, message_date, username, user_id)
                log_write(log_file, 'usr', text.encode('utf-8'), message_date, username, user_id)
            except UnicodeError:
                log_write(log_file, 'usr', 'UnicodeError', message_date, username, user_id)

            # Если получили комманду
            if text[0] == '/' and not give_answer:
                try:
                    if '@WikiReachBot' in text:
                        text = re.sub(r'@WikiReachBot', '', text)
                    if '/answer' in text:
                        text = re.sub(r'/answer ', '', text)
                        error_get, answer_text, reply_markup = commands_list['/answer'](
                            user_id in storage.data,
                            storage,
                            user_id, username, text)
                        error += error_get
                        give_answer = True

                    if not give_answer:
                        error_get, answer_text, reply_markup = commands_list.get(text)(
                            user_id in storage.data, storage,
                            user_id, username)
                        error += error_get

                except TypeError:
                    if user_id not in storage.data:
                        storage.new_user(username, user_id)
                    answer_text = dictionary['non_existent_command']
                give_answer = True

            # Если текстовый запрос, пытаемся понять его
            if not give_answer:
                error_get, answer_text, reply_markup = understand_text(user_id in storage.data,
                                                                       storage,
                                                                       user_id, username, text)
                error += error_get
                give_answer = True

            if error == '' or 'Wrong url' in error:

                if storage.data[user_id]['question'] == 'answer_article_id' or \
                                storage.data[user_id]['state'] == 'waitForStart':
                    del_msg = True
                else:
                    del_msg = False
                error += answer(log_file, storage, bot, user_id, chat_id, answer_text,
                                reply_markup, del_msg=False)
            else:
                print "err: "
                print error
                error = ''

            offset += 1  # id следующего обновления
        error += answer(log_file, storage, bot, 0, 0, '', None)
        time.sleep(0.01)

except KeyboardInterrupt:
    log_write(log_file, 'endl', '', sys_time())
    log_write(log_file, 'sys', 'Бот остановлен.', sys_time())
# except Exception:
#     log_write(log_file, 'sys', 'Неизвестная ошибка', sys_time())
finally:
    log_write(log_file, 'sys', '------------- Конец сеанса --------------\n\n\n', sys_time())
    log_file.close()
    storage.close_db()
