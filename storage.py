# coding=utf-8

# Здесь хранится информация текущей сессии: какие пользователи делали каие запросы и т.д.

class Storage:
    def __init__(self):
        self.data = dict()

    # Добавляет нового пользователя во временное хранилище данных
    def new_user(self, username, user_id):
        self.data[user_id] = {
            'username': username,
            'state': 'waitForStart',
            'game': ''
        }
