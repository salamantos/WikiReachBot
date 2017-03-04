# coding=utf-8

# Настраиваемые параметры бота

from commands import c_help, c_startg, c_endg, c_change_art, c_hitler_mode, c_score, c_open

bot_token = '353206446:AAEnwupmsYWkapfe3RLjRmCbJ4ZN_NNYJww'  # salamantos_first_bot
# bot_token = '312320944:AAHRVs-an8Jy0iTl9Q5sfzwPfv8GrwKuLV4'  # WikiReachBot

commands_list = {
    '/help': c_help,
    '/starth': c_startg,
    '/endg': c_endg,
    '/change_art': c_change_art,
    '/hitler_mode': c_hitler_mode,
    '/score': c_score,
    '/open': c_open
}

# print(commands_list.get('/help')())
