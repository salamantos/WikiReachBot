# coding=utf-8
import time


def sys_time():
    return time.time()


def log_write(scenario, action, log_time, user='', log_user_id=''):
    tuple_time = time.gmtime(log_time)
    # log_time = int(log_time)
    res_time = time.strftime('%Y-%m-%d %H:%M:%S', tuple_time)
    if scenario == 'usr':
        log_file.write(
            str(res_time) + ': @' + str(user) + ' (' + str(log_user_id) + ') написал: "' + str(action) + '"\n')
    elif scenario == 'bot':
        log_file.write(
            str(res_time) + ': ---> @' + str(user) + ' (' + str(log_user_id) + ') бот ответил: "' + str(action) +
            '"\n')
    elif scenario == 'sys':
        log_file.write(str(res_time) + ': ' + str(action) + '\n')
    elif scenario == 'endl':
        log_file.write('\n')

log_file = open('logs/logs.txt', 'a')
