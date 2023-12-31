import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from dotenv import load_dotenv, find_dotenv
import storage
import re
import json
import requests
from docx import Document
from datetime import datetime
import locale
from threading import Thread
locale.setlocale(locale.LC_ALL, "")


load_dotenv(find_dotenv())



token: str = os.getenv(key="VK_TOKEN")

vk_session: vk_api.VkApi = vk_api.VkApi(token=token)
vk = vk_session.get_api()
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

services = ["дистрибьюция", "сведение и мастеринг", "создание дизайна", "аренда бита", "создание трека"]
servicesDescriptions = ["Дистрибуция - публикация Вашего трека/Альбома на все цифровые площадки.\nКаждый релиз отправляется на модерацию ПРОМО всех стриминговых сервисов.\nСсылка на портфолио - (позже)\n\n⏳ Сроки: от 3 до 5 дней.",
                        "Сведение и Мастеринг - выполнение комплекса работ по постобработке музыкального произведения.\nОчистка и подготовка звуковых дорожек, Обработка вокала, Питч-коррекция. Добавление различных эффектов и особенностей, Расширение стереобазы, работа с панорамой, Эквализация и компрессия,  и многое другое.\nВсе Ваши пожелания и требования будут учтены в процессе работы. Вам доступно Три бесплатных правки итоговой работы.\nСсылка на портфолио - (позже)\n\n⏳ Сроки: от 3 до 5 дней.",
                        "Создание дизайна - Создание обложки для Релиза/Альбома, Ретушь и обработка фото, создание дизайна для ПРОМО.\nВсе Ваши пожелания и требования будут учтены в процессе работы. Вам доступно Три бесплатных правки итоговой работы.\nСсылка на портфолио - https://vk.com/album-221967488_295470314\n\n⏳ Сроки: от 3 до 5 дней.",
                        "Аренда бита - любая категория аренды бита, от MP3 до EXCLUSIVE. Все биты представленные в плейлистах доступны для покупки.\nПлейлисты разбиты по разным Авторам и  жанрам, выбирайте подходящий Вам звук.\n\nСсылка на плейлист 1 - (позже)\n\n⏳ Сроки: 1 день.",
                        "Создание трека - услуга в полном объеме временно недоступна.\n\n⏳ Сроки: по договорённости"]
servicesPrices = [500, 2500, 1500, 1500, 5000]

def sender(id: int, text: str, keyboard: VkKeyboard = None):
    post = {"user_id": id, "message": text, "random_id": 0}
    if keyboard is not None:
        post["keyboard"] = keyboard.get_keyboard()
    vk_session.method("messages.send", post)
#getHistory
def get_last_msg(peer_id: int, msg_id: int):
    post = {"peer_id": peer_id, "conversation_message_ids": [msg_id+2]}
    return vk_session.method("messages.getByConversationMessageId", post)

def get_ggg(peer_id: int, user_id: int, mid: int, msg: str):
    post = {"peer_id": peer_id, "user_id":user_id, "start_message_id":mid, "offset":-2}
    while vk_session.method("messages.getHistory", post)['items'][0]['text'] == msg:
        continue
    return vk_session.method("messages.getHistory", post)['items'][0]['text']

def get_info(id: int):
    post = {"user_ids": [id]}
    return vk_session.method("users.get", post)

def start_event(event):
    keyboard = VkKeyboard()
    keyboard.add_button(
        "Связаться с менеджером", VkKeyboardColor.POSITIVE
    )
    keyboard.add_line()
    keyboard.add_button("Услуги", VkKeyboardColor.NEGATIVE)
    keyboard.add_openlink_button("Отзывы", "https://vk.com/topic-221967488_49474380")
    keyboard.add_line()
    keyboard.add_openlink_button("О нас", "https://vk.com/@lvvlabel-kto-my")
    keyboard.add_openlink_button("FAQ", "https://vk.com/@lvvlabel-chastye-voprosy")
    sender(event.user_id, "Вот что мы можем вам предложить", keyboard)

def register(event):
    keyboard = VkKeyboard()
    keyboard.add_button("меню",VkKeyboardColor.SECONDARY)
    sender(event.user_id, "Введите свои паспортные данные в формате: серия номер",keyboard)
    creds = get_ggg(event.peer_id, event.user_id, event.message_id, "Введите свои паспортные данные в формате: серия номер")
    print(creds)
    match = re.search(r'^[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9][0-9][0-9]$', creds)
    if not match:
        sender(event.user_id, "Ошибка, проверьте правильность введенных данных",keyboard)
        return
    else:
        #sender(id, "окок",keyboard)
        passp = creds
    
    sender(event.user_id, "Введите свои дату и место регистрации в формате: 01.01.2007 название учреждения",keyboard)
    creds = get_ggg(event.peer_id, event.user_id, event.message_id+2, "Введите свои дату и место регистрации в формате: 01.01.2007 название учреждения")
    print(creds)
    match = re.search(r'^((3[0-1])|([1-2][0-9])|(0[1-9]))\.((1[0-2])|(0[1-9]))\.([0-9][0-9][0-9][0-9])\s', creds)
    if not match:
        print(match, creds)
        sender(event.user_id, "Ошибка, проверьте правильность введенных данных",keyboard)
        return
    else:
        #sender(id, "окок",keyboard)
        passp_cred = creds
    
    sender(event.user_id, "Введите свой номер телефона в формате: +79999999999",keyboard)
    creds = get_ggg(event.peer_id, event.user_id, event.message_id+4,"Введите свой номер телефона в формате: +79999999999")
    print(creds)
    match = re.search(r'^\+7[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', creds)
    if not match:
        sender(event.user_id, "Ошибка, проверьте правильность введенных данных",keyboard)
        return
    else:
        ##sender(id, "окок",keyboard)
        phone = creds
    
    sender(event.user_id, "Введите свой адрес",keyboard)
    creds = get_ggg(event.peer_id, event.user_id, event.message_id+6, "Введите свой адрес")
    print(creds)
    address = creds
    
    sender(event.user_id, "Введите свою фамилию имя отчество:",keyboard)
    creds = get_ggg(event.peer_id, event.user_id, event.message_id+8, "Введите свою фамилию имя отчество:")
    match = re.search(r'^[^\W\d_]+\s[^\W\d_]+?(\s[^\W\d_]+)$', creds)
    if not match:
        sender(event.user_id, "Ошибка, проверьте правильность введенных данных",keyboard)
        print(match, creds)
        return
    else:
        name = creds
        storage.create_user(
            role=0,
            address=address,
            phone=phone,
            full_name=name,
            passport=passp,
            login=passp_cred,
            vk_id=event.user_id
        )
        sender(event.user_id, "Вы зарегистрированы",keyboard)

def accept_order(event, prevService):
    id = event.user_id
    keyboard = VkKeyboard()
    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
    print("ВЫ выбрали услугу", services[prevService])
    if storage.check_user(vk_id=id):
        pass
    else:
        keyboard.add_button(
            "Регистрация", VkKeyboardColor.POSITIVE
        )
        sender(id, "Вам необходимо зарегестрироваться", keyboard)
        return
    
    sender(id, "Заполните документы и отправьте их модератору: @ghostikgh", keyboard)
    # Открываем документ
    doc = Document("sogl.docx")
    user = storage.get_user_vk_id(id)
    # Получаем все параграфы документа
    paras = doc.paragraphs
    
    today = datetime.now()
    
    print(user)
    
    # Проходим по всем параграфам и заменяем необходимые поля
    for para in paras:
        if "{{name}}" in para.text:
            para.text = para.text.replace("{{name}}", user[0][2].title())
    for para in paras:
        if "{{passport}}" in para.text:
            para.text = para.text.replace("{{passport}}", user[0][3])
    for para in paras:
        if "{{day}}" in para.text:
            para.text = para.text.replace("{{day}}", datetime.strftime(today, '%d'))
    for para in paras:
        if "{{month}}" in para.text:
            para.text = para.text.replace("{{month}}", datetime.strftime(today, ' %B'))
    for para in paras:
        if "{{year}}" in para.text:
            para.text = para.text.replace("{{year}}", datetime.strftime(today, '%Y'))
    for para in paras:
        if "{{pass_creds}}" in para.text:
            para.text = para.text.replace("{{pass_creds}}", user[0][0])
    for para in paras:
        if "{{address}}" in para.text:
            para.text = para.text.replace("{{address}}", user[0][4])

    # Сохраняем изменения
    doc.save("output.docx")
    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=event.peer_id)['upload_url'],
                                    files={'file': open('output.docx', 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title=f'Согласие_обработку_{user[0][2].title()}', tags=[])

    vk.messages.send(
        peer_id=event.peer_id,
        random_id=0,
        attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
    )
    
    doc = Document("dog.docx")
    user = storage.get_user_vk_id(event.user_id)
    # Получаем все параграфы документа
    paras = doc.paragraphs
    
    today = datetime.now()

    # Проходим по всем параграфам и заменяем необходимые поля
    for para in paras:
        if "{{name}}" in para.text:
            para.text = para.text.replace("{{name}}", user[0][2].title())
    for para in paras:
        if "{{passport}}" in para.text:
            para.text = para.text.replace("{{passport}}", user[0][3])
    for para in paras:
        if "{{day}}" in para.text:
            para.text = para.text.replace("{{day}}", datetime.strftime(today, '%d'))
    for para in paras:
        if "{{month}}" in para.text:
            para.text = para.text.replace("{{month}}", datetime.strftime(today, ' %B'))
    for para in paras:
        if "{{year}}" in para.text:
            para.text = para.text.replace("{{year}}", datetime.strftime(today, '%Y'))
    for para in paras:
        if "{{services}}" in para.text:
            para.text = para.text.replace("{{services}}", services[prevService])
    for para in paras:
        if "{{price}}" in para.text:
            para.text = para.text.replace("{{price}}", str(servicesPrices[prevService]))

    # Сохраняем изменения
    doc.save("output.docx")
    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=event.peer_id)['upload_url'],
                                    files={'file': open('output.docx', 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title=f'Договор_{user[0][2].title()}', tags=[])

    vk.messages.send(
        peer_id=event.peer_id,
        random_id=0,
        attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
    )
    


def start_vk_bot():
    prevService = -100
    print("Server in work")
    for event in longpoll.listen():
        
        if event.type == VkEventType.MESSAGE_NEW:
            
            if event.to_me:
                print(f'{event.text} from {event.user_id}')
                msg = event.text.lower()
                id = event.user_id
                
                if msg == "начать" or msg == "меню":
                    thread = Thread(target=start_event, args=[event])
                    thread.start()
                    
                if msg == "регистрация":
                    thread = Thread(target=register, args=[event])
                    thread.start()
                        
                if msg == "связаться с менеджером":
                    keyboard = VkKeyboard()
                    keyboard.add_button("Творческий/Примеры работ, оценка, услуги", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Юридический вопрос/Оформление документов", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Маркетинг/Реклама, продвижение", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Технический вопрос/Не работает сайт, бот", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Мы прочитаем ваш вопрос и ответим на него как можно скорее. Для удобства выберите тему вопроса.", keyboard)
                if msg == "творческий/примеры работ, оценка, услуги":
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Чем я могу вам помочь? Опишите свою проблему следующим сообщением", keyboard)
                if msg == "юридический вопрос/оформление документов":
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Чем я могу вам помочь? Опишите свою проблему следующим сообщением", keyboard)
                if msg == "маркетинг/реклама, продвижение":
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Чем я могу вам помочь? Опишите свою проблему следующим сообщением", keyboard)
                if msg == "технический вопрос/не работает сайт, бот":
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Чем я могу вам помочь? Опишите свою проблему следующим сообщением", keyboard)
                if msg == "услуги" or msg == "⏪назад⏪":
                    keyboard = VkKeyboard()
                    keyboard.add_button("Дистрибьюция", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Сведение и Мастеринг", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Создание Дизайна", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Аренда Бита", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Создание трека", VkKeyboardColor.SECONDARY)
                    keyboard.add_line()
                    keyboard.add_button("Узнать про пакеты", VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Выберите услугу", keyboard)
                for i in range(len(services)):
                    if msg == services[i]:
                        prevService = i
                        keyboard = VkKeyboard()
                        keyboard.add_button("✅Подтвердить заказ✅", VkKeyboardColor.POSITIVE)
                        keyboard.add_line()
                        keyboard.add_button("⏪Назад⏪")
                        sender(id, f"{servicesDescriptions[i]}\n💸 Цена: от {servicesPrices[i]} ₽.", keyboard)
                        break
                if msg == "узнать про пакеты":
                    keyboard = VkKeyboard()
                    keyboard.add_button("Меню", VkKeyboardColor.NEGATIVE)
                    sender(id, "Ваш Запрос в работе, в ближайшее время с вами свяжется менеджер", keyboard)
                if msg == "✅подтвердить заказ✅":
                    if prevService >= 0:
                        thread = Thread(target=accept_order, args=(event, prevService))
                        thread.start()
                    else:
                        sender(id, "Ошибка пройдите процедуру заново", keyboard)