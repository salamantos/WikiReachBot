# coding=utf-8

import time
from functions import sys_time, log_write, write_bot_name, recognize_update, get_updates_for_bot, commands_list, \
    storage, answer, log_file, init_bot, understand_text
import settings
from settings import dictionary

# Включение бота
log_write('sys', '------------- Начало сеанса -------------', sys_time())
bot = init_bot(settings.bot_token)
write_bot_name(bot)

# log_file.close()  # Fix it!

print 'successfully'
# Запуск прослушки Телеграма
offset = 0
try:
    answer_text = u'<Заготовка под ответ>'
    while True:
        # TypeError: 'NoneType' object is not iterable
        updates = get_updates_for_bot(bot, offset)  # Если нет обновлений, вернет пустой список
        for update in updates:
            # Получаем информацию о сообщении
            offset, user_id, username, text, message_date = recognize_update(update)
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
                    answer_text = commands_list.get(text)(user_id in storage.data, storage, user_id, username)

                except TypeError:
                    answer_text = dictionary['non_existent_command']
                give_answer = True

            # Если текстовый запрос, пытаемся понять его
            if not give_answer:
                answer_text = understand_text(user_id in storage.data, storage, user_id, username, text)

                give_answer = True

            answer(bot, user_id, answer_text)
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
