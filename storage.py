# coding=utf-8

# Здесь хранится информация текущей сессии: какие пользователи делали каие запросы и т.д.

class Storage:
    def __init__(self):
        self.data = dict()
        self.data = {
            109029852: {
                'username': 'salamantos',
                'last_user_action': '',
                'bot_answer_should_be': ''
            }
        }

    # Добавляет нового пользователя во временное хранилище данных
    def new_user(self, username, user_id):
        self.data[user_id] = {
            'username': username,
            'last_user_action': '',
            'bot_answer_should_be': ''
        }
