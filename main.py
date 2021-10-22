from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps

updater = Updater("2053878260:AAFD95fDkO9g3ov9uCW2INKZwlEYnBqs7GA", use_context=True)
dispatcher = updater.dispatcher


def admin_restriction(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        bot = update.message.bot
        message = update.message
        status = bot.get_chat_member(message.chat_id, message.from_user.id).status
        if status != 'creator' and status != 'administrator':
            name = update.message.from_user.name
            print("Unauthorized access denied for {}.".format(name))
            return
        return func(update, context, *args, **kwargs)

    return wrapped


@admin_restriction
def hammer_setup(update, context):
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text(text='please set a regexp: /hammer {your_regexp}')
    else:
        context.user_data[str(chat_id) + '_regexp'] = context.args[0]
        context.user_data[str(chat_id) + '_auditor'] = update.message.from_user.id
        update.message.reply_text(text='you configuration has been set, the requester is auditor')


# todo to finish this it's needed to find how to get user chat_id by it's name
@admin_restriction
def audit_user_setup(update, context):
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text(text='please send user name: /audit @username')
    else:
        context.user_data[str(chat_id) + '_auditor'] = context.args[0]
        update.message.reply_text(text='you audit configuration has been set')


@admin_restriction
def start_hammer(update, context):
    chat_id = update.effective_chat.id
    regexp = context.user_data.get(str(chat_id) + '_regexp')
    if regexp is not None:
        dispatcher.add_handler(MessageHandler(Filters.chat_type.groups & Filters.regex(regexp), ban_and_revoke_messages))
    else:
        update.message.reply_text(text='please, configure hammer at first: /hammer {your_regexp}')


@admin_restriction
def get_config(update, context):
    chat_id = update.effective_chat.id
    regexp = context.user_data.get(str(chat_id) + '_regexp')
    auditor = context.user_data.get(str(chat_id) + '_auditor')
    if regexp is None and auditor is None:
        update.message.reply_text(text='please, configure hammer at first: /hammer')
    else:
        update.message.reply_text(text='Current configuration to this group: regexp: ' + regexp + ', auditor: ' + update.message.bot.getChat(auditor).username)


@admin_restriction
def ban_and_revoke_messages(update, context):
    bot = update.message.bot
    message = update.message
    name = update.message.from_user.name
    chat_id = update.effective_chat.id
    auditor = context.user_data.get(str(chat_id) + '_auditor')
    bot.send_message(chat_id=auditor, text="Banning {}".format(name))
    print("Received a valid by the regexp message, banning {}".format(name))
    # update.message.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

    # report spam //not implemented on telegram API
    # ban user and revoke all the messages
    bot.ban_chat_member(chat_id=message.chat_id, user_id=message.from_user.id, revoke_messages=True)


def main():
    """Chat Hammer bot is starting"""

    dispatcher.add_handler(CommandHandler("hammer", hammer_setup))
    dispatcher.add_handler(CommandHandler("start", start_hammer))
    dispatcher.add_handler(CommandHandler("config", get_config))

    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
