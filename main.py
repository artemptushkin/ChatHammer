from telegram import  ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# bot = telegram.Bot(token='2053878260:AAFD95fDkO9g3ov9uCW2INKZwlEYnBqs7GA')

keyboard = [
    ["🔨Hammer", "⚙️ My setups"]
]


def hello(update, context):
    update.message.reply_text('hi! ' + context.args[0])

def echo(update, context):
    update.message.reply_text(update.message.text)

def menu(update, context):
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text='Here comes the menu', reply_markup=reply_markup)

def echoToGroup(update, context):
    bot = update.message.bot
    message = update.message
    # update.message.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

    # report spam //not implemented on telegram API
    # ban user and revoke all the messages
    bot.ban_chat_member(chat_id=message.chat_id, user_id=message.from_user.id, revoke_messages=True)


def main():
    """Chat Hammer bot is starting"""
    updater = Updater("2053878260:AAFD95fDkO9g3ov9uCW2INKZwlEYnBqs7GA", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hello", hello))

    dispatcher.add_handler(MessageHandler(Filters.chat_type.groups & Filters.regex(r"(bit\.ly|cuti.cc).*"), echoToGroup))
    dispatcher.add_handler(MessageHandler(Filters.chat_type.private, menu))

    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
