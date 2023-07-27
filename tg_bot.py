import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from logger import TelegramLogHandler
from vk_bot import detect_intent_texts

logger = logging.getLogger(__name__)


def generic_response(update: Update, context: CallbackContext, project_id) -> None:
    session_id = update.effective_chat.id
    flow_response = detect_intent_texts(project_id, session_id, update.message.text)
    update.message.reply_text(flow_response.query_result.fulfillment_text)


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    telegram_token_log = os.environ["TELEGRAM_TOKEN_LOG"]
    dialogflow_project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    tg_chat_id_log = os.environ["TG_CHAT_ID"]

    bot = Bot(token=telegram_token_log)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, tg_chat_id_log))

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    send_response_with_project_id = partial(generic_response, project_id=dialogflow_project_id)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_response_with_project_id))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
