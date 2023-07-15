import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from telegram import Bot
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent import detect_intent_texts
from logger import TelegramLogHandler

logger = logging.getLogger(__name__)


def generic_response(event, vk_api, project_id):
    user_id = event.user_id
    message = event.text
    flow_response = detect_intent_texts(project_id=project_id,
                                        session_id=user_id,
                                        text=message)
    if not flow_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=flow_response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()

    vk_token = os.environ['VK_APIKEY']
    telegram_token_logs = os.environ['TELEGRAM_TOKEN_LOG']
    tg_chat_id = os.environ['TG_CHAT_ID_LOG']

    dialogflow_project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    bot = Bot(token=telegram_token_logs)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, tg_chat_id))

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            generic_response(event, vk_api, dialogflow_project_id)
