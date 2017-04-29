# coding: utf8

import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль логов
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def sys_time():
    return time.time()


def log_write(log_file, scenario, action, user='', log_user_id=''):
    log_time = sys_time()
    tuple_time = time.gmtime(log_time)
    # log_time = int(log_time)
    res_time = time.strftime('%Y-%m-%d %H:%M:%S', tuple_time)
    if scenario == 'usr':
        log_file.write('{0}: @{1} ({2}) написал: "{3}"\n'.format(
            res_time, user, log_user_id, action))
    elif scenario == 'bot':
        log_file.write('{0}: ---> @{1} ({2}) бот ответил: "{3}"\n'.format(
            str(res_time), user, log_user_id, action))
    elif scenario == 'sys':
        log_file.write('{0}: {1}\n'.format(res_time, action))
    elif scenario == 'endl':
        log_file.write('\n')
