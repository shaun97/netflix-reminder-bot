import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import psycopg2
import sql_functions as sf

PORT = int(os.environ.get('PORT', 5000))
DATABASE_URL = os.environ['DATABASE_URL']
TOKEN = os.environ['BOT_TOKEN']

# Connect to DB
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    first_name = update.message.from_user.first_name

    sf.insert_user(conn, user_id, user_name, first_name)
    update.message.reply_text(f'Hello {first_name}, my name is Xenia and I am here to provide friendly reminders! :)')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type /register to register your username to the bot to start receiving monthly reminders.')

def register_reminder(update, context):
    user_id = update.message.from_user.id
    is_reminder_on = sf.toggle_reminder(conn, user_id)
    if is_reminder_on:
        msg = "on"
    else:
        msg = "off"
    update.message.reply_text(f'Your reminders has been turned {msg}')

def general(update, context):
    print(update.message.text)
    msg = update.message.text
    user_id = update.message.from_user.id

    if msg == "I am xenia":
        sf.set_admin(conn, user_id)
        update.message.reply_text("Hello Xenia")
    else:
        update.message.reply_text("Hello friends, my name is Xenia and I am here to provide friendly reminders! :) Type /start to begin")

# Xenia commands

def set_message(update, context):
    #check admin before doing anything
    pass
def set_frequency(update, context):
    pass
def set_time(update, context):
    pass
def set_remindees(update, context):
    pass

def view_remindees(update, context):
    pass

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # General commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reminder", register_reminder))

    # Xenia commands
    dp.add_handler(CommandHandler("set_message", set_message))
    dp.add_handler(CommandHandler("set_frequency", set_frequency))
    dp.add_handler(CommandHandler("set_time", set_time))
    dp.add_handler(CommandHandler("set_remindees", set_remindees))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, general))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook('https://afternoon-brushlands-18615.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()