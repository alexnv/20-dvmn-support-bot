import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from telegram import Bot
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent import detect_intent_texts
from logger import TelegramLogHandler

logger = logging.getLogger('Logger')


def echo(event, vk_api, project_id):
    user_id = event.user_id
    message = event.text
    flowresponse = detect_intent_texts(project_id=project_id,
                                       session_id=user_id,
                                       text=message)
    if not flowresponse.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=flowresponse.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()

    VK_TOKEN = os.environ['VK_APIKEY']
    TELEGRAM_TOKEN_LOGS = os.environ['TELEGRAM_TOKEN_LOG']
    TG_CHAT_ID = os.environ['TG_CHAT_ID_LOG']

    dialogflow_project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    bot = Bot(token=TELEGRAM_TOKEN_LOGS)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, TG_CHAT_ID))

    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, dialogflow_project_id)
