# coding=utf-8

import time
# import re
# import wiki_parser
from telegram_connection import recognize_update, answer, init_bot
from log_writer import log_write, sys_time

from settings import bot_token, commands_list

# Инициализация сеанса
log_file = open('logs/logs.txt', 'a')
log_write('sys', '------------- Начало сеанса -------------', sys_time())
bot = init_bot(bot_token)
log_write('sys', bot.username + '\n', sys_time())

# print(type(bot))
# print(bot.username)
text = commands_list.get('/help')()

exit(0)

# answer(281389974, 'Ты пидор!')
offset = 0
try:
    while True:
        updates = bot.get_updates(offset).wait()  # Если нет обновлений, вернет пустой список
        for update in updates:
            # Распознаем команду
            offset, user_id, username, text, message_date = recognize_update(update)

            # Логи
            log_write('usr', update, message_date, username, user_id)
            log_write('usr', text.encode('utf-8'), message_date, username, user_id)

            if text is None:
                text = 'Вы не написали текста, сеньор!'.decode('utf-8')
            # log_write('В сообщении номер ' + str(offset) + ' пользователь ' + str(username) +
            #                ' с id ' + str(user_id) + ' написал: "' + text.encode('utf-8') + '"')
            answer_text = text
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
    log_file.close()
