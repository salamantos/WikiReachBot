# coding=utf-8

# Реализация комманд бота
# Порядок аргументов: session_continues, storage, user_id


def c_help():
    return u'Справка по командам:'


def c_startg(session_continues, storage, user_id):
    if not session_continues or storage.data[user_id]['station'] == 'waitForStart':
        # return init_game()
        pass
    else:
        return u'Вы уже начали игру :)'


def c_endg(session_continues, storage, user_id):
    if not session_continues or storage.data[user_id]['station'] == 'game':
        pass

def c_change_art():
    print('help')


def c_hitler_mode():
    print('help')


def c_score():
    print('help')


def c_open():
    print('help')
