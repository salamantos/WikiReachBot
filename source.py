# coding=utf-8

import re
from bot_commands import commands_list, understand_text
from storage import Storage
from settings import *
from Telegram_requests import *

# Включение бота
reset_messages = 'y'  # raw_input('Reset messages? y/n\n')
if reset_messages == 'y':
    reset_messages = True
else:
    reset_messages = False

try:
    log_file = open('logs/logs.txt', 'a')
except Exception, err_exception:
    sys.stderr.write('error: {}'.format(err_exception))
    exit(1)
log_write(log_file, 'sys', '------------- Начало сеанса -------------')
bot = init_bot(BOT_TOKEN)
try:
    write_bot_name(log_file, bot)
    log_write(log_file, 'sys', 'Successfully started')
except FatalError:
    log_write(log_file, 'sys', FatalError.txt)
    exit(1)
storage = Storage()
offset = 0

# Пропускаем пропущенные сообщения
if reset_messages:
    updates = get_updates_for_bot(bot, offset)
    if updates:
        try:
            with open('logs/reset_file.txt', 'a') as reset_file:
                reset_file.write(str(updates))
        except Exception, err_exception:
            sys.stderr.write('error: {}'.format(err_exception))
            exit(1)

        offset = updates[-1].update_id + 1

log_write(log_file, 'sys', 'Successfully skipped messages')

# Запуск прослушки Телеграма
try:
    answer_text = u'<Заготовка под ответ>'
    reply_markup = None
    while True:
        # Отлавиваем только EasyError, остальное завершает работу
        try:
            updates = get_updates_for_bot(bot, offset)  # Если нет обновлений, вернет пустой список
            for update in updates:
                # Получаем информацию о сообщении
                offset, user_id, chat_id, username, text, message_date = extract_update_info(
                    update)
                give_answer = False  # Готов ли ответ

                # Если не текстовое сообщение
                if text is None:
                    text = u'(Нет текста)'
                    answer_text = NO_TEXT
                    give_answer = True

                # Логи
                try:
                    log_write(log_file, 'usr', update, username, user_id)
                    log_write(log_file, 'usr', text.encode('utf-8'), username, user_id)
                except UnicodeError:
                    log_write(log_file, 'usr', 'UnicodeError', username, user_id)

                # Если получили комманду
                if text[0] == '/' and not give_answer:
                    try:
                        if '@WikiReachBot' in text:
                            text = re.sub(r'@WikiReachBot', '', text)
                        if '/answer' in text:
                            text = re.sub(r'/answer ', '', text)
                            answer_text, reply_markup = commands_list['/answer'](
                                user_id in storage.data,
                                storage,
                                user_id, username, text)
                            give_answer = True

                        if not give_answer:
                            answer_text, reply_markup = commands_list.get(text)(
                                user_id in storage.data, storage,
                                user_id, username)

                    except TypeError:
                        if user_id not in storage.data:
                            storage.new_user(username, user_id)
                        answer_text = NON_EXISTENT_COMMAND
                    give_answer = True

                # Если текстовый запрос, пытаемся понять его
                if not give_answer:
                    answer_text, reply_markup = understand_text(user_id in storage.data,
                                                                storage,
                                                                user_id, username, text)
                    give_answer = True

                if storage.data[user_id]['question'] == 'answer_article_id' or \
                                storage.data[user_id]['state'] == 'waitForStart':
                    del_msg = True
                else:
                    del_msg = False
                answer(log_file, storage, bot, user_id, chat_id, answer_text,
                       reply_markup, del_msg=False)

                offset += 1  # id следующего обновления
            answer(log_file, storage, bot, 0, 0, '', None)
            time.sleep(0.01)
        except ContinueError:
            answer(log_file, storage, bot, user_id, chat_id, ContinueError.txt,
                   reply_markup, del_msg=False)

            offset += 1  # id следующего обновления
        except EasyError:
            offset += 1
            log_write(log_file, 'sys', EasyError.txt)

except KeyboardInterrupt:
    log_write(log_file, 'endl', '')
    log_write(log_file, 'sys', 'Бот остановлен.')
# except Exception:
#     log_write(log_file, 'sys', 'Неизвестная ошибка', sys_time())
except FatalError:
    log_write(log_file, 'sys', FatalError.txt)
finally:
    log_write(log_file, 'sys', '------------- Конец сеанса --------------\n\n\n')
    log_file.close()
    storage.close_db()
