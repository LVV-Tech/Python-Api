import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

token: str = os.getenv(key="VK_TOKEN")

vk_session: vk_api.VkApi = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def sender(id: int, text: str):
    vk_session.method("messages.send", {"user_id": id, "message": text, "random_id": 0})


def start_vk_bot():
    print("Server in work")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print(event.text)
            if event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == "начать":
                    sender(id, "Вот что мы можем вам предложить")

