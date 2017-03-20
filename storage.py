# coding=utf-8

import settings
import MySQLdb
import secret_settings


# Здесь хранится информация текущей сессии: какие пользователи делали какие запросы и т.д.
class Storage:
    def __init__(self):
        self.data = dict()

        # подключаемся к базе данных
        self.db = MySQLdb.connect(host=secret_settings.host, user=secret_settings.user, passwd=secret_settings.passwd,
                                  db=secret_settings.db)
        self.db.set_character_set('utf8')
        # формируем курсор, с помощью которого можно исполнять SQL-запросы
        self.cursor = self.db.cursor()

    # Добавляет нового пользователя во временное хранилище данных
    def new_user(self, username, user_id):
        self.data[user_id] = {
            'username': username,
            'state': 'waitForStart',
            'question': '',  # Когда просим ответить на каой-то вопрос (какую статью сделать целевой)
            'game': {},
            'last_message_sent': 0,
            'temp_data': '',
            'goal_article_url': settings.default_article_url,
            'goal_article_header': settings.default_article_header,
            'difficulty': settings.default_difficulty,
            'games_count': 0,
            'games_won': 0
        }

        self.db_sync_download(user_id)

    def modify_local_storage(self, user_id, state=None, question=None, game=None, last_message_sent=None,
                             goal_article_url=None, goal_article_header=None, difficulty=None, temp_data=None):
        if state is not None:
            self.data[user_id]['state'] = state
        if question is not None:
            self.data[user_id]['question'] = question
        if game is not None:
            self.data[user_id]['game'] = game
        if last_message_sent is not None:
            self.data[user_id]['last_message_sent'] = last_message_sent
        if goal_article_url is not None:
            self.data[user_id]['goal_article_url'] = goal_article_url
        if goal_article_header is not None:
            self.data[user_id]['goal_article_header'] = goal_article_header
        if difficulty is not None:
            self.data[user_id]['difficulty'] = difficulty
        if temp_data is not None:
            self.data[user_id]['temp_data'] = temp_data

        error = self.db_sync_upload(user_id)
        return error

    def db_sync_upload(self, user_id, games_won=None):
        # Количество выигранных/проигранных игр обновляется отдельно от остальных данных!!!
        error = ''
        try:
            if user_id not in self.data:
                sql = "SELECT * FROM user_storage WHERE user_id = %(user_id)s" % {"user_id": user_id}
                self.db.ping(True)
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                if len(result) == 0:
                    sql = """INSERT INTO user_storage
                         (user_id, username, goal_article_url, goal_article_header, difficulty)
                         VALUES ('%(user_id)s', '%(username)s', '%(goal_article_url)s',
                         '%(goal_article_header)s', '%(difficulty)s')
                      """ % {"user_id": user_id,
                             "username": self.data[user_id]['username'],
                             "goal_article_url": self.data[user_id]['goal_article_url'],
                             "goal_article_header": self.data[user_id]['goal_article_header'],
                             "difficulty": self.data[user_id]['difficulty']
                             }
                    self.db.ping(True)
                    # Исполняем SQL-запрос
                    self.cursor.execute(sql)
                    # Применяем изменения к базе данных
                    self.db.commit()
                    return error

            if games_won is not None:
                self.data[user_id]['games_count'] += 1
                if games_won:
                    self.data[user_id]['games_won'] += 1
                    sql = """UPDATE user_storage SET
                                         games_count = games_count + 1,
                                         games_won = games_won + 1"""
                else:
                    sql = 'UPDATE user_storage SET games_count = games_count + 1'
            else:
                sql = """UPDATE user_storage
                                     SET
                                     username = '%(username)s',
                                     goal_article_url = '%(goal_article_url)s',
                                     goal_article_header = '%(goal_article_header)s',
                                     difficulty = '%(difficulty)s'
                                     WHERE user_id = '%(user_id)s'
                                  """ % {"user_id": user_id,
                                         "username": self.data[user_id]['username'],
                                         "goal_article_url": self.data[user_id]['goal_article_url'],
                                         "goal_article_header": self.data[user_id]['goal_article_header'],
                                         "difficulty": self.data[user_id]['difficulty']
                                         }
            # Проверяем соединение и переподключаемся, если нужно
            self.db.ping(True)
            # Исполняем SQL-запрос
            self.cursor.execute(sql)
            # Применяем изменения к базе данных
            self.db.commit()
        except ZeroDivisionError:  # (AttributeError, MySQLdb.OperationalError):
            error = 'DB connection error'
            print error
        return error

    def db_sync_download(self, user_id):
        error = ''
        try:
            sql = "SELECT * FROM user_storage WHERE user_id = %(user_id)s" % {"user_id": user_id}
            self.db.ping(True)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                sql = """INSERT INTO user_storage
                     (user_id, username, goal_article_url, goal_article_header, difficulty)
                     VALUES ('%(user_id)s', '%(username)s', '%(goal_article_url)s',
                     '%(goal_article_header)s', '%(difficulty)s')
                  """ % {"user_id": user_id,
                         "username": self.data[user_id]['username'],
                         "goal_article_url": self.data[user_id]['goal_article_url'],
                         "goal_article_header": self.data[user_id]['goal_article_header'],
                         "difficulty": self.data[user_id]['difficulty']
                         }
                self.db.ping(True)
                # Исполняем SQL-запрос
                self.cursor.execute(sql)
                # Применяем изменения к базе данных
                self.db.commit()
                return error

            sql = """SELECT * FROM user_storage
                     WHERE user_id = '%(user_id)s'
                  """ % {"user_id": user_id}
            # Проверяем соединение и переподключаемся, если нужно
            self.db.ping(True)
            # Исполняем SQL-запрос
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) < 0:
                error = 'SQL download data error'
                return error
            self.data[user_id]['username'] = result[0][2]
            self.data[user_id]['goal_article_url'] = result[0][3]
            self.data[user_id]['goal_article_header'] = result[0][4]
            self.data[user_id]['difficulty'] = result[0][5]
            self.data[user_id]['games_count'] = result[0][6]
            self.data[user_id]['games_won'] = result[0][7]
        except (AttributeError, MySQLdb.OperationalError):
            error = 'DB connection error'
            print error
        return error

    def close_db(self):
        self.db.close()

    def del_user(self, user_id):
        # del (self.data[user_id])
        self.new_user(self, user_id)
