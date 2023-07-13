import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from logger import TelegramLogHandler
from vk_bot import detect_intent_texts

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def echo(update: Update, context: CallbackContext, project_id) -> None:
    session_id = update.effective_chat.id
    flowresponse = detect_intent_texts(project_id, session_id, update.message.text)
    update.message.reply_text(flowresponse.query_result.fulfillment_text)


def main() -> None:
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    telegram_token_log = os.environ["TELEGRAM_TOKEN_LOG"]
    dialogflow_project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    TG_CHAT_ID_LOG = os.environ["TG_CHAT_ID"]

    """Start the bot."""
    bot = Bot(token=telegram_token_log)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, TG_CHAT_ID_LOG))

    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on non command i.e message - echo the message on Telegram
    send_response_with_project_id = partial(echo, project_id=dialogflow_project_id)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_response_with_project_id))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
