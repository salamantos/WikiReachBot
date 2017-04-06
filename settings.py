# coding=utf-8

# Настраиваемые параметры бота

# bot_token = '353206446:AAEnwupmsYWkapfe3RLjRmCbJ4ZN_NNYJww'  # salamantos_first_bot
bot_token = '312320944:AAHRVs-an8Jy0iTl9Q5sfzwPfv8GrwKuLV4'  # WikiReachBot

url_prefix = u'https://ru.wikipedia.org'  # https://ru.wikipedia.org/wiki/Кошка
search_template_prefix = u'https://ru.wikipedia.org/w/index.php?search='
search_template_postfix = u'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F%3A%D0%9F%D0%BE%D0%B8%D1%81' \
                          u'%D0%BA&go=%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D1%82%D0%B8 '

max_links_count = 100
max_messages_count = 5  # Если 5 или меньше, выводим полностью
split_messages_count = 3  # Если больше max_messages_count, выводим первые 3 и спрашиваем, нужно ли еще

timeout_personal_messages = 1.5  # seconds
big_timeout_personal_messages = 25

default_difficulty = 4

difficulty_list = {
    u'Hard\n(3 перехода)': 3,
    u'Normal\n(4 перехода)': 4,
    u'Easy\n(5 переходов)': 5
}

keyboard = [
    [u'Hard\n(3 перехода)', u'Normal\n(4 перехода)', u'Easy\n(5 переходов)'],
    [u'Отмена']
]

black_list = [u'Редактировать раздел', u'Википедия', u'Ссылки на источники',
              u'(Страница отсутствует)', u'(страница отсутствует)',
              u'Просмотр этого шаблона', u'Служебная:', u'Шаблон:', u'Увеличить', u'Ethnologue']

dictionary = {
    'no_text': u'Вы не написали текста, сударь (сударыня? o_O)',
    'non_existent_command': u'Такой команды нет :с',
    'this_is_links_list': u'Вот список ссылок по статье ',
    'your_goal_is': u'\n(Вам нужно дойти до статьи\n',
    'what_you_want_to_choose': u'Напишите номер выбранной ссылки',
    'goal_article_was_changed': u'Целевая статья успешно изменена на ',
    'enter_article_link': u'Введите название статьи или ссылку на неё',
    'congratulations': u'Поздравляю, вы победили за ',
    'steps': u' ходов!',
    'no_more_steps': u'У вас закончились ходы, но статья ',
    'not_reached': u' не достигнута',
    'steps_made': u'\n\nУже сделано ходов: ',
    'hello_at_start': u'Привет! Справка по командам: /help',
    'game_already_started': u'Вы уже начали игру :)',
    'give_answer': u'Ответьте на вопрос, плез',
    'you_not_play': u'Вы не играете сейчас в игру',
    'game_stopped': u'Игра завершена',
    'cant_change_article_while_playing': u'Нельзя сменить целевую статью во время игры',
    'invite_to_start': u'Хотите начать игру?\nНаберите /start_game или посмотрите /help для справки по командам',
    'wrong_entered_url': u'Ссылка не работает, попробуйте снова',
    'opening_just_while_playing': u'Открыть статью можно только во время игры',
    'wrong_id': u'Неверный номер',
    'cant_change_difficulty_while_playing': u'Нельзя сменить сложность во время игры',
    'difficulty_was_changed': u'Сложность успешно изменена на ',
    'wrong_entered_difficulty': u'Плез, выберите верное значение на появившейся клавиатуре',
    'select_difficulty': u'Выберите сложноть на появившейся клавиатуре',
    'selecting_difficulty_canceled': u'Отменено, вы можете начать игру: /start_game',
    'commands_help': u'''Справка по командам:\n
/rules - Узнать правила игры
/help - Помощь по командам
/start_game - Начать игру
/end_game - Закончить текущую игру
/answer - ответить (нужно для групповых чатов): answer <Ваш ответ>
/change_article - Выбрать статью, до которой нужно добраться
/hitler_mode - REACH HITLER!
/set_difficulty - Настроить сложность игры
/open - Открыть статью в Википедии''',
    'rules': [u'''Привет!
Правила очень простые:
# Я выдаю вам все ссылки из случайной статьи Википедии
# Ваша задача - переходя по этим ссылкам дойти до целевой статьи
# Целевая статья назвается ''',
              u''' (её можно сменить)
# Количество ходов ограничено: нужно уложиться в ''',
              u''' переходов (тоже можно поменять)
# Собственно, всё :D

P.S. Не пугайтесь, если ссылок больше 1000, это нормально))'''],
    'score1': u'Игр сыграно: ',
    'score2': u'\nВы победили в ',
    'score3': u' из них',
    'open_to_get_link': u'Введите номер статьи из списка',
    'you_canceled_article': u'Вы отменили выбор',
    'articles_found': u'Найденные статьи:\n',
    'select_article_or_cancel': u'\nВыберите нужную или наберите cancel для отмены',
    'choose_or_need_more': u'Показана чать ссылок. Напишите номер выбранной ссылки или more, чтобы загрузить еще',
    'more_links': u'Еще ссылки:\n'
}

# entities=[MessageEntity(type=u'bold', offset=0, length=3, url=None, user=None)]

random_page_link = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6' \
                   '%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87' \
                   '%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0' \
                   '%D0%BD%D0%B8%D1%86%D0%B0 '

default_article_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%88%D0%BA%D0%B0'
default_article_header = u'Кошка'

hitler_article_url = 'https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D1%82%D0%BB%D0%B5%D1%80,' \
                     '_%D0%90%D0%B4%D0%BE%D0%BB%D1%8C%D1%84 '
hitler_article_header = u'Гитлер, Адольф'

default_article_url = hitler_article_url
default_article_header = hitler_article_header

# Error prefixes:
# ut - update type - Если пришло не сообщение

# "Update(update_id=525719033, message=Message(message_id=1687, sender=User(id=109029852, first_name=u'Matvey',
# last_name=u'Volkov', username=u'salamantos'), date=1489183404, edit_date=None, chat=Chat(id=109029852,
# type=u'private', title=None, username=u'salamantos', first_name=u'Matvey', last_name=u'Volkov'), forward_from=User(
# id=93372553, first_name=u'BotFather', last_name=None, username=u'BotFather'), forward_from_chat=None,
# forward_date=1488892912, reply_to_message=None, text=u"I can help you create and manage Telegram bots. If you're
# new to the Bot API, please see the manual.\n\nYou can control me by sending these commands:\n\n/newbot - create a
# new bot\n/mybots - edit your bots [beta]\n/mygames - edit your games [beta]\n\nEdit Bots\n/setname - change a bot's
#  name\n/setdescription - change bot description\n/setabouttext - change bot about info\n/setuserpic - change bot
# profile photo\n/setcommands - change the list of commands\n/deletebot - delete a bot\n\nBot Settings\n/token -
# generate authorization token\n/revoke - revoke bot access token\n/setinline - toggle inline mode\n/setinlinegeo -
# toggle inline location requests\n/setinlinefeedback - change inline feedback settings\n/setjoingroups - can your
# bot be added to groups?\n/setprivacy - toggle privacy mode in groups\n\nGames\n/newgame - create a new
# game\n/listgames - get a list of your games\n/editgame - edit a game\n/deletegame - delete an existing game",
# entities=[MessageEntity(type=u'text_link', offset=85, length=14, url=u'https://core.telegram.org/bots', user=None),
#  MessageEntity(type=u'bot_command', offset=149, length=7, url=None, user=None), MessageEntity(type=u'bot_command',
# offset=176, length=7, url=None, user=None), MessageEntity(type=u'bold', offset=201, length=6, url=None, user=None),
#  MessageEntity(type=u'bot_command', offset=208, length=8, url=None, user=None), MessageEntity(type=u'text_link',
# offset=229, length=5, url=u'https://core.telegram.org/bots/games', user=None), MessageEntity(type=u'bold',
# offset=235, length=6, url=None, user=None), MessageEntity(type=u'bold', offset=243, length=9, url=None, user=None),
#  MessageEntity(type=u'bot_command', offset=253, length=8, url=None, user=None), MessageEntity(type=u'bot_command',
# offset=284, length=15, url=None, user=None), MessageEntity(type=u'bot_command', offset=325, length=13, url=None,
# user=None), MessageEntity(type=u'bot_command', offset=363, length=11, url=None, user=None), MessageEntity(
# type=u'bot_command', offset=402, length=12, url=None, user=None), MessageEntity(type=u'bot_command', offset=445,
# length=10, url=None, user=None), MessageEntity(type=u'bold', offset=472, length=12, url=None, user=None),
# MessageEntity(type=u'bot_command', offset=485, length=6, url=None, user=None), MessageEntity(type=u'bot_command',
# offset=523, length=7, url=None, user=None), MessageEntity(type=u'bot_command', offset=557, length=10, url=None,
# user=None), MessageEntity(type=u'text_link', offset=577, length=11, url=u'https://core.telegram.org/bots/inline',
# user=None), MessageEntity(type=u'bot_command', offset=589, length=13, url=None, user=None), MessageEntity(
# type=u'text_link', offset=619, length=17, url=u'https://core.telegram.org/bots/inline#location-based-results',
# user=None), MessageEntity(type=u'bot_command', offset=637, length=18, url=None, user=None), MessageEntity(
# type=u'text_link', offset=665, length=15, url=u'https://core.telegram.org/bots/inline#collecting-feedback',
# user=None), MessageEntity(type=u'bot_command', offset=690, length=14, url=None, user=None), MessageEntity(
# type=u'bot_command', offset=740, length=11, url=None, user=None), MessageEntity(type=u'text_link', offset=761,
# length=12, url=u'https://core.telegram.org/bots#privacy-mode', user=None), MessageEntity(type=u'bold', offset=785,
# length=5, url=None, user=None), MessageEntity(type=u'bot_command', offset=791, length=8, url=None, user=None),
# MessageEntity(type=u'text_link', offset=815, length=4, url=u'https://core.telegram.org/bots/games', user=None),
# MessageEntity(type=u'bot_command', offset=820, length=10, url=None, user=None), MessageEntity(type=u'bot_command',
# offset=858, length=9, url=None, user=None), MessageEntity(type=u'bot_command', offset=882, length=11, url=None,
# user=None)], audio=None, document=None, photo=None, sticker=None, video=None, voice=None, caption=None,
# contact=None, location=None, venue=None, new_chat_member=None, left_chat_member=None, new_chat_title=None,
# new_chat_photo=None, delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None,
# channel_chat_created=None, migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None),
# edited_message=None, inline_query=None, chosen_inline_result=None, callback_query=None)"
