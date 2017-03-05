# coding=utf-8

import settings

# Здесь хранится информация текущей сессии: какие пользователи делали каие запросы и т.д.

class Storage:
    def __init__(self):
        self.data = dict()

    # Добавляет нового пользователя во временное хранилище данных
    def new_user(self, username, user_id):
        self.data[user_id] = {
            'username': username,
            'state': 'waitForStart',
            'question': '',  # Когда просим ответить на каой-то вопрос (какую статью сделать целевой)
            'game': {},
            'goal_article_url': settings.default_article_url,
            'goal_article_header': settings.default_article_header
        }

    def del_user(self, user_id):
        del(self.data[user_id])
