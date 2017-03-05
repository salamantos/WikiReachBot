from twx.botapi import TelegramBot, ReplyKeyboardMarkup

bot_token = '353206446:AAEnwupmsYWkapfe3RLjRmCbJ4ZN_NNYJww'

bot = TelegramBot(bot_token)
bot.update_bot_info().wait()
print(bot.username)

# Send a message to a user
user_id = int(109029852)

# result = bot.send_message(user_id, 'test message body').wait()
# print(result)

"""
Get updates sent to the bot
"""
offset = 894829147  # id which will be first in list

updates = bot.get_updates(offset).wait()
for update in updates:
    print(update)

"""
Use a custom keyboard
"""
keyboard = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
         ['0']
]
reply_markup = ReplyKeyboardMarkup.create(keyboard)

# bot.send_message(user_id, 'please enter a number', reply_markup=reply_markup).wait()

# Update(
#   update_id=894829143, message=Message(
#       message_id=3, sender=User(
#           id=109029852, first_name=u'Matvey', last_name=u'Volkov',
#           username=u'salamantos'),
#       date=1488569622, edit_date=None, chat=Chat(
#           id=109029852, type=u'private', title=None, username=u'salamantos',
#           first_name=u'Matvey', last_name=u'Volkov'),
#       forward_from=None,
#       forward_from_chat=None, forward_date=None, reply_to_message=None,
#       text=u'dratuti)))', entities=None, audio=None, document=None,
#       photo=None, sticker=None, video=None, voice=None, caption=None,
#       contact=None, location=None, venue=None, new_chat_member=None,
#       left_chat_member=None, new_chat_title=None, new_chat_photo=None,
#       delete_chat_photo=None,
#       group_chat_created=None, supergroup_chat_created=None,
#       channel_chat_created=None, migrate_to_chat_id=None,
#       migrate_from_chat_id=None, pinned_message=None),
#   edited_message=None,
#   inline_query=None, chosen_inline_result=None, callback_query=None)


# Update(update_id=894829216, message=Message(message_id=134, sender=User(id=281389974, first_name=u'Quasar',
# last_name=None, username=u'quasa'), date=1488576793, edit_date=None, chat=Chat(id=281389974, type=u'private',
# title=None, username=u'quasa', first_name=u'Quasar', last_name=None), forward_from=None, forward_from_chat=None,
# forward_date=None, reply_to_message=None, text=u'TI PIDOR V STIKERI NE MOZHESH', entities=None, audio=None,
# document=None, photo=None, sticker=None, video=None, voice=None, caption=None, contact=None, location=None,
# venue=None, new_chat_member=None, left_chat_member=None, new_chat_title=None, new_chat_photo=None,
# delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None,
# migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None), edited_message=None, inline_query=None,
# chosen_inline_result=None, callback_query=None)
