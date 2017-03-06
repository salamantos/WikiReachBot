# coding=utf-8

# Настраиваемые параметры бота

# bot_token = '353206446:AAEnwupmsYWkapfe3RLjRmCbJ4ZN_NNYJww'  # salamantos_first_bot
bot_token = '312320944:AAHRVs-an8Jy0iTl9Q5sfzwPfv8GrwKuLV4'  # WikiReachBot

url_prefix = u'https://ru.wikipedia.org'  # https://ru.wikipedia.org/wiki/Кошка
search_template_prefix = u'https://ru.wikipedia.org/w/index.php?search='
search_template_postfix = u'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F%3A%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&go=%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D1%82%D0%B8'

max_links_count = 100

black_list = [u'Редактировать раздел', u'Википедия', u'Ссылки на источники',
              u'(Страница отсутствует)', u'(страница отсутствует)',
              u'Просмотр этого шаблона', u'Служебная:', u'Шаблон:']

dictionary = {
    'no_text': u'(Нет текста)',
    'non_existent_command': u'Такой команды нет :с',
    'this_is_links_list': u'Вот список ссылок по статье ',
    'your_goal_is': u'\n(Вам нужно дойти до статьи\n',
    'what_you_want_to_choose': u')\n\nЧто выбираете?',
    'goal_article_was_changed': u'Целевая статья успешно изменена на ',
    'enter_article_link': u'Введите ссылку на статью',
    'congratulations': u'Поздравляю, вы победили за ',
    'steps': u' ходов!',
    'no_more_steps': u'У вас закончились ходы, но статья ',
    'not_reached': u' не достигнута',
    'steps_made': u'\n\nУже сделано ходов: ',
    'hello_at_start': u'Привет! Справка по командам: /help',
    'commands_help': u'Справка по командам:',
    'game_already_started': u'Вы уже начали игру :)',
    'give_answer': u'Ответьте на вопрос, плез',
    'you_not_play': u'Вы не играете сейчас в игру',
    'game_stopped': u'Игра завершена',
    'cant_change_article_while_playing': u'Нельзя сменить целевую статью во время игры',
    'invite_to_start': u'Хотите начать игру?\nНаберите /start_game или посмотрите /help для справки по командам',
    'wrong_entered_url': u'Ссылка не работает, попробуйте снова',
    'opening_just_while_playing': u'Открыть статью можно только во время игры',
    'wrong_id': u'Неверный номер'
}

random_page_link = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6' \
                   '%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87' \
                   '%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0' \
                   '%D0%BD%D0%B8%D1%86%D0%B0 '

default_article_url = 'https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D1%82%D0%BB%D0%B5%D1%80,' \
                 '_%D0%90%D0%B4%D0%BE%D0%BB%D1%8C%D1%84 '
default_article_header = u'Гитлер, Адольф'

hitler_article_url = 'https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D1%82%D0%BB%D0%B5%D1%80,' \
                 '_%D0%90%D0%B4%D0%BE%D0%BB%D1%8C%D1%84 '
hitler_article_header = u'Гитлер, Адольф'
