import os.path
import shutil
from email import message_from_file

import requests
import telebot
import cv2
from telebot import types
from telebot.apihelper import send_message
from ultralytics import YOLO, solutions
from moviepy.editor import VideoFileClip
from Config_BD import repo
from mapHandler import mark_from_db, mark, mark_from_well_db
import datetime

from test import image

print("СТАРТУЕМ")
print("маг")

#model = YOLO("weights/best.pt")
#model = YOLO("weights/weights12/best.pt")
model = YOLO("weights/weights121225/best.pt")

model_well = YOLO("weights_well/best.pt")
bot = telebot.TeleBot('6412797520:AAEhE-O7L5otKppHBDKu5XFQjH740jYOgjA')
location_token = 'pk.d93bd73df995d45f948bf8edd36b1e3e'
sql = repo.SQL()
status = ["Рассматривается 🔁", "Выполняется 🔸", "Выполнена ✅", "Ошибка ⚠️"]
mark_from_db()
mark_from_well_db()
if os.path.exists("runs/result"):
    shutil.rmtree("runs/result")

@bot.message_handler(commands=['start'])
def button(message):
    if sql.get_role(message.chat.id) is not None:
        role = sql.get_role(message.chat.id)[0]
    else:
        role = "user"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile = types.KeyboardButton("Профиль 💬")
    application = types.KeyboardButton("Оставить заявку 🖇")
    finished_projects = types.KeyboardButton("Наши проекты ✅")
    application_open_well = types.KeyboardButton("Заявка на открытый колодец 🕳")
    information = types.KeyboardButton("Информация 🔔")
    share_telegram_bot = types.KeyboardButton("Поделиться Fixing holes Telegram Bot🚀🚀")
    markup.add(profile, information, finished_projects, application_open_well, application)
    if role == "admin":
        admin = types.KeyboardButton("Администратор 👤")
        markup.add(share_telegram_bot, admin)
    else:
        markup.add(share_telegram_bot)
    user_id = message.chat.id
    user_name = message.from_user.last_name
    if sql.users_select(user_id) is None:
        print('new user')
        sql.users_insert(user_name, user_id)
    video_file = open("утёнок из телеграмма🦆.mp4", "rb")
    video_data = video_file.read()
    bot.send_video(message.chat.id, video_data,
                   caption=f'<b>Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! Fixing_holes_Telegram_Bot готов к работе:</b>',
                   reply_markup=markup, parse_mode="html")
    video_file.close()


@bot.message_handler(content_types=['text'])
def func(message):
    if sql.get_role(message.chat.id) is not None:
        role = sql.get_role(message.chat.id)[0]
    else:
        role = "user"
    if message.text == "Администратор 👤" and role == "admin":
        answer_admin = types.InlineKeyboardMarkup(row_width=2)
        button_admin = types.InlineKeyboardButton("Администратор 👤", callback_data='Администратор 👤')
        answer_admin.add(button_admin)
        bot.send_message(message.chat.id, "🤖🤖🤖🤖🤖", reply_markup=answer_admin)

    if message.text == "Профиль 💬":
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user_id = message.from_user.id
        hole_count = sql.hole_count(user_id)
        well_count = sql.well_count(user_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_contact = types.KeyboardButton("Поделится своим номером телефона:", request_contact=True)
        markup.add(button_contact)
        back_button = types.KeyboardButton('↪️ Назад в меню')
        markup.add(back_button)
        answer_profile = types.InlineKeyboardMarkup(row_width=2)
        button_well_profile = types.InlineKeyboardButton("Заявки колодцы🕳", callback_data='профиль колодцы')
        button_pothole_profile = types.InlineKeyboardButton("Заявки ямы 🖇", callback_data='профиль ямы')
        button_profile_well_map = types.InlineKeyboardButton("📍 Карта 🕳", web_app=types.WebAppInfo(
            url=f"https://naughtily-hot-genet.cloudpub.ru/well/{user_id}"))
        button_profile_pothole_map = types.InlineKeyboardButton("📍 Карта 🖇", web_app=types.WebAppInfo(
            url=f"https://naughtily-hot-genet.cloudpub.ru/pothole/{user_id}"))

        answer_profile.add(button_well_profile, button_pothole_profile, button_profile_well_map,button_profile_pothole_map)
        bot.send_message(message.chat.id, f"<b>Ваше имя: {first_name} {last_name}</b>"
                                          f"\n<b>Ваш ID: {user_id}</b>"
                                          f"\n<b>Количество заявок на открытый колодец 🕳: {well_count}</b>"
                                          f"\n<b>Количество заявок на дорожный дефект 🖇: {hole_count}</b>"
                                          f"\n<b>История отправленных заявок:</b>", reply_markup=answer_profile,
                         parse_mode="html")
        bot.send_message(message.chat.id, f"\n<b>Поделитесь своим номером телефона: ☎️</b>", reply_markup=markup,
                         parse_mode="html")

    if message.text == "Оставить заявку 🖇":
        answer = types.InlineKeyboardMarkup(row_width=2)
        button_application = types.InlineKeyboardButton("заявка", callback_data='заявка')
        answer.add(button_application)
        bot.send_message(message.chat.id, "Оставьте заявку!", reply_markup=answer)

    if message.text == "Наши проекты ✅":
        bot.send_message(message.chat.id, "<b>Вот результат нашей работы!\nДО:</b>", parse_mode="html")
        photo_before = open("nah_project.jpg", "rb")
        photo_before_result = photo_before.read()
        bot.send_photo(message.chat.id, photo_before_result, caption="<b>Анализ фото из заявки:</b>", parse_mode="html")
        photo_analysis = open("nah_project_result.jpg", "rb")
        photo_analysis_result = photo_analysis.read()
        bot.send_photo(message.chat.id, photo_analysis_result, caption="<b>После:</b>", parse_mode="html")
        photo_after = open("nah_project_after.jpg", "rb")
        photo_after_result = photo_after.read()
        bot.send_photo(message.chat.id, photo_after_result,
                       caption="<b>Благодарим каждого неравнодушного пользователя за направленные заявки.</b>"
                               "\n<b>Безопасность на дороге - это наша общая задача! 🌍</b>"
                               "\n<b>Мы сотрудничаем с Росавтодор: анализируем ваши заявки, направляем и контролируем их выполнение. ✅</b>"
                               "\n<b>При возникновение вопросов, звоните по номеру телефона: 8-950-111-25-01 ☎️</b>",
                       parse_mode="html")

    if message.text == "Заявка на открытый колодец 🕳":
        answer = types.InlineKeyboardMarkup(row_width=2)
        button_application = types.InlineKeyboardButton("заявка", callback_data='заявка на открытый колодец')
        answer.add(button_application)
        bot.send_message(message.chat.id, "<b>Заявка на открытый колодец 🕳</b>", reply_markup=answer,
                         parse_mode="html")

    if message.text == "Информация 🔔":
        # f = open("html/map.html")
        # bot.send_document(message.chat.id, f)
        bot.send_message(message.chat.id, "<b>На данный момент актуальной информации нет! 💬</b>", parse_mode="html")

    if message.text == '↪️ Назад в меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profile = types.KeyboardButton("Профиль 💬")
        application = types.KeyboardButton("Оставить заявку 🖇")
        finished_projects = types.KeyboardButton("Наши проекты ✅")
        application_open_well = types.KeyboardButton("Заявка на открытый колодец 🕳")
        information = types.KeyboardButton("Информация 🔔")
        share_telegram_bot = types.KeyboardButton("Поделиться Fixing holes Telegram Bot🚀🚀")
        markup.add(profile, information, finished_projects, application_open_well, application)
        if role == "admin":
            admin = types.KeyboardButton("Администратор 👤")
            markup.add(share_telegram_bot, admin)
        else:
            markup.add(share_telegram_bot)
        bot.send_message(message.chat.id, "📲", reply_markup=markup)

    if message.text == "Поделиться Fixing holes Telegram Bot🚀🚀":
        photo_share = open("Qr_code.png", "rb")
        photo_share_read = photo_share.read()
        bot.send_photo(message.chat.id, photo_share_read, caption=f'<b>QR-код Fixing_holes_Telegram Bot</b>',
                       parse_mode="html")
        markup_qr = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button_qr = types.KeyboardButton('↪️ Назад в меню')
        markup_qr.add(back_button_qr)
        bot.send_message(message.chat.id, "<b><code>https://t.me/Fixing_holes_Telegram_Bot</code></b>",
                         parse_mode="HTML",
                         reply_markup=markup_qr)


mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_photo = types.KeyboardButton("фото")
button_video = types.KeyboardButton("видео")
button_application = types.KeyboardButton("заявка")
button_contact = types.KeyboardButton("контакт")
mm.add(button_photo, button_video)
mm.add(button_application)
mm.add(button_contact)
button_well = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_well_photo = types.KeyboardButton("фото")
button_well_video = types.KeyboardButton("видео")
button_well_application = types.KeyboardButton("заявка")
button_well.add(button_well_photo, button_well_video)
button_well.add(button_well_application)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    user_id = message.from_user.id
    user_phone = message.contact.phone_number
    bot.send_message(user_id, f"<b>Ваш номер телефона: {user_phone}</b>", parse_mode="html")
    if user_phone[0] == '7':
        user_phone = '+' + user_phone
    if user_phone[0] == '8':
        user_phone = '+7' + user_phone[1:-1]
    sql.add_number(user_phone, user_id)

@bot.message_handler(func=lambda message: True, content_types=['location'])
def loc_photo(message, photo, det_photo, mode):
    location = message.location
    print(type(location))
    lat = location.latitude
    long = location.longitude
    mark_from_db()
    headers = {"Accept-Language": "ru"}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={location_token}&lat={lat}&lon={long}&format=json',
        headers=headers).json()
    date = datetime.datetime.now()
    bot.send_message(message.chat.id, address.get("display_name"))
    if mode == 1:
        sql.pathole_app_insert(address.get("display_name"), long, lat, message.chat.id, photo, det_photo, date)
        app_id_pathole = sql.get_last_ph_id_by_userid(message.chat.id)
        bot.send_message(message.chat.id,
                         f"<b>Спасибо за вашу бдительность, заявка №{app_id_pathole} принята и будет направленна в Росавтодор! ✅</b>"
                         "\n<b>Ждем от Вас новых заявок!</b>❤ ️", parse_mode="html")
    elif mode == 2:
        sql.well_app_insert(address.get("display_name"), long, lat, message.chat.id, photo, det_photo, date)
        app_id_well = sql.get_last_well_id_by_userid(message.chat.id)
        bot.send_message(message.chat.id,
                         f"<b>Спасибо за вашу бдительность, заявка №{app_id_well} принята и будет направленна в Водоканал! ✅</b>"
                         "\n<b>Ждем от Вас новых заявок!</b>❤ ️", parse_mode="html")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def photo_well(message):
    photo = message.photo
    fileID = photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_info.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    photo = open(file_info.file_path, 'rb').read()
    bot.send_message(message.chat.id, "<b>️Идет анализ вашего фото. Подождите!</b>⏱ ️", parse_mode="html")
    res = model_well(file_info.file_path, save=True, project="runs/result", name=fileID)
    open_w = 0
    clse_w = 0
    for i in range(len(res[0].boxes.cls)):
        if res[0].boxes.cls[i] == 16:
            open_w += 1
        if res[0].boxes.cls[i] == 15:
            clse_w += 1
    if open_w:  # проверка на обнаружения открытого колодца
        file_name = file_info.file_path.replace("photos/", "")
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
        answer = types.InlineKeyboardMarkup(row_width=2)
        answer.add(button)
        bot.send_photo(message.chat.id, detect_photo, reply_markup=answer)
        #det_photo = open(f"runs/result/bot/{file_name}", "rb").read()
        det_photo = open(f"runs/result/{fileID}/{file_name}", "rb").read()
        bot.register_next_step_handler(message, loc_photo, photo, det_photo, 2)
    elif clse_w:
        file_name = file_info.file_path.replace("photos/", "")
        #detect_photo = open(f"runs/result/bot/{file_name}", "rb")
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        bot.send_photo(message.chat.id, detect_photo)
        bot.send_message(message.chat.id,
                         "<b>На фото не обнаружено открытых колодцев! ⚠️ Ваша заявка не будет направленна в Водоканал. ❌</b>"
                         "\n<b>Спасибо за бдительность! Если вы не согласны, обратитесь по номеру телефона: 8-950-111-25-01. ☎️</b>"
                         "\n<b>Ждем от Вас новых заявок!</b>❤ ️", parse_mode="html")
    else:
        bot.send_message(message.chat.id,
                         "<b>На фото не обнаружено ни одного колодца! ⚠️ Заявка не будет направленна в Водоканал. ❌</b>",
                         parse_mode="html")

# @bot.message_handler(func=lambda message: True, content_types=['video'])
# def video_well(message):
    # video = message.video
    # fileID = video.file_id
    # file_info = bot.get_file(fileID)
    # downloaded_file = bot.download_file(file_info.file_path)
    # os.makedirs("videos", exist_ok=True)
    # with open(file_info.file_path, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    # bot.send_message(message.chat.id, "<b>Идет анализ вашего видео. Подождите!</b>⏱ ", parse_mode="html")
    # res = model_well(file_info.file_path, save=True, project="runs/result", name=fileID)
    # file_name = file_info.file_path.replace("videos/", "")
    # input_video_path = f"runs/result/{fileID}/{file_name}".replace(".mp4", ".avi")
    # output_video_path = input_video_path.replace('.avi', '.mp4')
    # print(input_video_path)
    # print(output_video_path)
    # clip = VideoFileClip(input_video_path)
    # clip.write_videofile(output_video_path)
    # bot.send_video(message.chat.id, video=open(output_video_path, 'rb'))
    # with open("video.jpg", "rb") as image_file:
    #     photo = image_file.read()
    #     bot.register_next_step_handler(message, loc_photo, photo, photo, 2)

    #подсчет колодцем открытых и закрытых
    # video = message.video
    # fileID = video.file_id
    # file_path = os.path.join("videos", f"{fileID}.mp4")
    # file_info = bot.get_file(fileID)
    # downloaded_file = bot.download_file(file_info.file_path)
    # os.makedirs("videos", exist_ok=True)
    # with open(file_path, "wb") as new_file:
    #     new_file.write(downloaded_file)
    # cap = cv2.VideoCapture(file_path)
    # bot.send_message(message.chat.id,
    #                  "<b>Идет анализ вашего видео. Подождите!</b>⏱ ", parse_mode="html")
    # w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    # # region_points = [(0, (int)(h * 0.8)), (w, (int)(h * 0.8)), (w, (int)(h * 0.8 - 10)), (0, (int)(h * 0.8 - 10))]
    # region_points = [(0, (int)(h * 0.7)), (w, (int)(h * 0.7)), (w, (int)(h * 0.95)), (0, (int)(h * 0.95))]
    # video_writer = cv2.VideoWriter("counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    # counter = solutions.ObjectCounter(
    #     show_in=True,
    #     show_out=False,
    #     region=region_points,
    #     classes=[0,1],
    #     line_width=2,
    #     model=model_well,
    #     conf=0.5
    #     # conf = 0.8
    #     # conf = 0.4
    # )
    # while cap.isOpened():
    #     success, im0 = cap.read()
    #     if not success:
    #         print("sc")
    #         break
    #
    #     results = counter(im0)
    #     video_writer.write(results.plot_im)
    #
    # cap.release()
    #
    # video_writer.release()
    # cv2.destroyAllWindows()
    #
    # output_mp4 = "counting_output.mp4"
    # clip = VideoFileClip("counting_output.avi")
    # clip.write_videofile(output_mp4, codec='libx264', audio=False)
    #
    # if results.in_count > 0:
    #     with open("video.jpg", "rb") as image_file:
    #
    #         button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
    #         answer = types.InlineKeyboardMarkup(row_width=2)
    #         answer.add(button)
    #         bot.send_video(message.chat.id, video=open(output_mp4, 'rb'), reply_markup=answer)
    #
    #         os.remove(output_mp4)
    #         os.remove("counting_output.avi")
    #         os.remove(file_path)
    #
    #         photo = image_file.read()
    #         bot.register_next_step_handler(message, loc_photo, photo, photo, 2)
    # else:
    #
    #     bot.send_video(message.chat.id, video=open(output_mp4, 'rb'))
    #     bot.send_message(message.chat.id,
    #                      "<b>На видео не обнаружено ни одного колодца! ⚠️ Заявка не будет направленна в Водоканал. ❌</b>",
    #                      parse_mode="html")
    #     bot.send_message(message.chat.id,
    #                      "<b>Спасибо, за бдительность! Если вы несогласны, обратитесь по номеру телефона: 8-950-111-25-01 ☎️</b>"
    #                      "\n<b>Безопасность на дорогах - это наша общая задача! 🌍</b>"
    #                      "\n<b>Ждем от Вас новых заявок!</b>❤ ", parse_mode="html")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def detect_photo(message):
    photo = message.photo
    fileID = photo[-1].file_id
    file_info = bot.get_file(fileID)
    file_name = file_info.file_path.replace("photos/", "")
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_info.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    photo = open(file_info.file_path, 'rb').read()
    bot.send_message(message.chat.id,
                     "<b>Идет анализ вашего фото. Подождите!</b>⏱ ", parse_mode="html")
    res = model(file_info.file_path, save=True, project="runs/result", name=fileID)
    if k := len(res[0].boxes):
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        det_photo = open(f"runs/result/{fileID}/{file_name}", "rb").read()
        if k == 1:
            bot.send_message(message.chat.id, f"<b>Обнаружена {k} яма</b>", parse_mode="html")
            button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
            answer = types.InlineKeyboardMarkup(row_width=2)
            answer.add(button)
            bot.send_photo(message.chat.id, detect_photo, reply_markup=answer)

        elif (k > 1) and (k < 5):
            bot.send_message(message.chat.id, f"<b>Обнаружено {k} ямы</b>", parse_mode="html")
            button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
            answer = types.InlineKeyboardMarkup(row_width=2)
            answer.add(button)
            bot.send_photo(message.chat.id, detect_photo, reply_markup=answer)

        elif k > 5:
            bot.send_message(message.chat.id, f"<b>Обнаружено {k} ям</b>", parse_mode="html")
            button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
            answer = types.InlineKeyboardMarkup(row_width=2)
            answer.add(button)
            bot.send_photo(message.chat.id, detect_photo, reply_markup=answer)

        bot.register_next_step_handler(message, loc_photo, photo, det_photo, 1)

    else:
        #file_name = file_info.file_path.replace("photos/", "")
        # print(file_name)
        # detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        # bot.send_photo(message.chat.id, detect_photo)

        bot.send_message(message.chat.id,
                         "<b>На фото не обнаружено дорожных дефектов (ям)! ⚠️ Ваша заявка не будет направленна в Росавтодор. ❌</b>",
                         parse_mode="html")
        bot.send_message(message.chat.id,
                         "<b>Спасибо, за бдительность! Если вы несогласны, обратитесь по номеру телефона: 8-950-111-25-01 ☎️</b>"
                         "\n<b>Безопасность на дорогах - это наша общая задача! 🌍</b>"
                         "\n<b>Ждем от Вас новых заявок!</b>❤ ", parse_mode="html")

@bot.message_handler(func=lambda message: True, content_types=['video'])
def detect_video(message):
    video = message.video
    fileID = video.file_id
    file_path = os.path.join("videos", f"{fileID}.mp4")
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("videos", exist_ok=True)
    with open(file_path, "wb") as new_file:
        new_file.write(downloaded_file)
    cap = cv2.VideoCapture(file_path)
    bot.send_message(message.chat.id,
                     "<b>Идет анализ вашего видео. Подождите!</b>⏱ ", parse_mode="html")
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    #region_points = [(0, (int)(h * 0.8)), (w, (int)(h * 0.8)), (w, (int)(h * 0.8 - 10)), (0, (int)(h * 0.8 - 10))]
    region_points = [(0, (int)(h * 0.7)), (w, (int)(h * 0.7)), (w, (int)(h * 0.95)), (0, (int)(h * 0.95))]
    video_writer = cv2.VideoWriter("counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    counter = solutions.ObjectCounter(
        show_in=True,
        show_out = False,
        region=region_points,
        classes=[0],
        line_width=2,
        model = model,
        conf = 0.5
        #conf = 0.8
        #conf = 0.4
    )
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("sc")
            break

        results = counter(im0)
        video_writer.write(results.plot_im)

    cap.release()

    video_writer.release()
    cv2.destroyAllWindows()

    output_mp4 = "counting_output.mp4"
    clip = VideoFileClip("counting_output.avi")
    clip.write_videofile(output_mp4, codec='libx264', audio=False)

    if results.in_count > 0:
        with open("video.jpg", "rb") as image_file:

            if results.in_count == 1:
                bot.send_message(message.chat.id, f"<b>Обнаружена {results.in_count} яма</b>", parse_mode="html")


            elif (results.in_count > 1) and (results.in_count < 5):
                bot.send_message(message.chat.id, f"<b>Обнаружено {results.in_count} ямы</b>", parse_mode="html")


            elif results.in_count > 5:
                bot.send_message(message.chat.id, f"<b>Обнаружено {results.in_count} ям</b>", parse_mode="html")

            button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
            answer = types.InlineKeyboardMarkup(row_width=2)
            answer.add(button)
            bot.send_video(message.chat.id, video=open(output_mp4, 'rb'), reply_markup=answer)
            os.remove(output_mp4)
            os.remove("counting_output.avi")
            os.remove(file_path)

            photo = image_file.read()
            bot.register_next_step_handler(message, loc_photo, photo, photo, 1)
    else:
        bot.send_video(message.chat.id, video=open(output_mp4, 'rb'))
        bot.send_message(message.chat.id,
                         "<b>На видео не обнаружено дорожных дефектов (ям)! ⚠️ Ваша заявка не будет направленна в Росавтодор. ❌</b>",
                         parse_mode="html")
        bot.send_message(message.chat.id,
                         "<b>Спасибо, за бдительность! Если вы несогласны, обратитесь по номеру телефона: 8-950-111-25-01 ☎️</b>"
                         "\n<b>Безопасность на дорогах - это наша общая задача! 🌍</b>"
                         "\n<b>Ждем от Вас новых заявок!</b>❤ ", parse_mode="html")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "заявка":
                answer = types.InlineKeyboardMarkup(row_width=2)
                button_photo = types.InlineKeyboardButton("фото", callback_data='фото')
                button_video = types.InlineKeyboardButton("видео", callback_data='видео')
                answer.add(button_photo, button_video)
                bot.send_message(call.message.chat.id, f"<b>Вы хотите прикрепить фото или видео?</b>",
                                 reply_markup=answer, parse_mode="html")

            if call.data == "фото":
                bot.send_message(call.message.chat.id, "<b>Прикрепите фото. 📸</b>", parse_mode="html")
                bot.register_next_step_handler(call.message, detect_photo)


            if call.data == "видео":
                bot.send_message(call.message.chat.id, "<b>Прикрепите видео. 🎥</b>", parse_mode="html")
                bot.register_next_step_handler(call.message, detect_video)

            if call.data == 'геопозиция':
                bot.send_message(call.message.chat.id, "<b>Прикрепите геопозицию, где вы обнаружили дефект.🌐</b>",
                                 parse_mode="html")

            if call.data == 'контакт':
                bot.send_message(call.message.chat.id, "<b>Поделитесь своим номером телефона:</b>", parse_mode="html")

            if call.data == "заявка на открытый колодец":
                answer = types.InlineKeyboardMarkup(row_width=2)
                button_photo_well = types.InlineKeyboardButton("фото", callback_data='фото колодец')
                button_video_well = types.InlineKeyboardButton("видео", callback_data='видео колодец')
                answer.add(button_photo_well, button_video_well)
                bot.send_message(call.message.chat.id, f"<b>Вы хотите прикрепить фото или видео?</b>",
                                 reply_markup=answer, parse_mode="html")

            if call.data == "фото колодец":
                bot.send_message(call.message.chat.id, "<b>Прикрепите фото. 📸</b>", parse_mode="html")
                bot.register_next_step_handler(call.message, photo_well)

            if call.data == "видео колодец":
                bot.send_message(call.message.chat.id, "<b>Прикрепите видео. 🎥</b>", parse_mode="html")
                bot.send_message(call.message.chat.id, "<b>Видео подсчет колодцев на данный момент не работает 🎥</b>", parse_mode="html")
                # bot.register_next_step_handler(call.message, video_well)

            if call.data == 'ссылка':
                link = 'https://t.me/Fixing_holes_Telegram_Bot'
                bot.send_message(call.message.chat.id, f"{link}")

            if call.data == "Администратор 👤":
                answer_admin = types.InlineKeyboardMarkup(row_width=2)
                button_admin_well = types.InlineKeyboardButton("Заявки на колодцы", callback_data='admin_well')

                button_admin_well_map = types.InlineKeyboardButton("📍 Карта 🕳", web_app=types.WebAppInfo(url="https://naughtily-hot-genet.cloudpub.ru/well"))

                button_admin_pothole = types.InlineKeyboardButton("Заявки на ямы", callback_data='admin_pothole')

                button_admin_pothole_map = types.InlineKeyboardButton("📍 Карта 🖇", web_app=types.WebAppInfo(url="https://naughtily-hot-genet.cloudpub.ru/pothole"))

                answer_admin.add(button_admin_well, button_admin_pothole, button_admin_well_map,
                                 button_admin_pothole_map)
                bot.send_message(call.message.chat.id, f"<b>Данные о каких заявках вам нужны?</b>",
                                 reply_markup=answer_admin, parse_mode="html")

            if call.data == "admin_well":
                usernames = sql.get_all_username()
                answer = types.InlineKeyboardMarkup(row_width=2)
                for username in usernames:
                    b = types.InlineKeyboardButton(username[0], callback_data=f"user_well{username[1]}")
                    answer.add(b)
                bot.send_message(call.message.chat.id, f"<b>Пользователи: </b>", reply_markup=answer, parse_mode="html")

            if call.data.startswith("user_well"):
                user_id = int(call.data.replace("user_well", ""))
                apps = sql.get_all_well_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row_pothole = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row_pothole.append(types.InlineKeyboardButton(app[0], callback_data=f"app_well{app[0]}"))
                    else:
                        ans.row(*button_row_pothole)
                        c = 1
                        button_row_pothole = []
                        button_row_pothole.append(types.InlineKeyboardButton(app[0], callback_data=f"app_well{app[0]}"))
                if button_row_pothole != []:
                    ans.row(*button_row_pothole)
                if button_row_pothole == []:
                    message = f"<b>У данного пользователя нет заявок на открытые колодцы!</b>"
                    bot.send_message(call.message.chat.id, message, reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Отправленные заявки на открытые колодцы:\n{message}</b>", reply_markup=ans,
                                     parse_mode="html")

            if call.data.startswith("app_well"):
                app_id = int(call.data.replace("app_well", ""))
                app = sql.get_well_by_id(app_id)
                message = "🔰<b>Заявка №</b>" + str(app[0]) + "\t🕳\nСтатус заявки: " + app[
                    8] + "\n🌐 Место положение:\n" + \
                          app[1] + "\n⏰ Дата и время:\n" + str(app[7]) + "\n"
                ans = types.InlineKeyboardMarkup()
                for i in range(len(status)):
                    button = types.InlineKeyboardButton(status[i], callback_data=f"edit_well{app_id}_{i}")
                    ans.add(button)
                bot.send_photo(call.message.chat.id, app[6], f"<b>{message}\nВыберите статус заявки 📝: </b>",
                               reply_markup=ans, parse_mode="html")

            if call.data.startswith("edit_well"):
                d = call.data.replace("edit_well", "")
                list = d.split("_")
                app_id = int(list[0])
                new_status = int(list[1])
                sql.update_status_well(app_id, status[new_status])
                mark_from_well_db()
                message = f"<b>Новый статус заявки №{app_id}: {status[new_status]}</b>"
                bot.send_message(call.message.chat.id, message, parse_mode="html")

            if call.data == "admin_pothole":
                usernames = sql.get_all_username()
                answer = types.InlineKeyboardMarkup(row_width=2)
                for username in usernames:
                    b = types.InlineKeyboardButton(username[0], callback_data=f"user_pothole{username[1]}")
                    answer.add(b)
                bot.send_message(call.message.chat.id, f"<b>Пользователи: </b>", reply_markup=answer, parse_mode="html")

            if call.data.startswith("user_pothole"):
                user_id = int(call.data.replace("user_pothole", ""))
                apps = sql.get_all_ph_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row_pothole = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_pothole{app[0]}"))
                    else:
                        ans.row(*button_row_pothole)
                        c = 1
                        button_row_pothole = []
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_pothole{app[0]}"))
                if button_row_pothole != []:
                    ans.row(*button_row_pothole)
                if button_row_pothole == []:
                    message = f"<b>У данного пользователя нет заявок на ямы!</b>"
                    bot.send_message(call.message.chat.id, message, reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id, f"<b>Отправленные заявки на ямы:\n{message}</b>",
                                     reply_markup=ans, parse_mode="html")

            if call.data.startswith("app_pothole"):
                app_id = int(call.data.replace("app_pothole", ""))
                app = sql.get_ph_by_id(app_id)
                message = "🔰<b>Заявка №</b>" + str(app[0]) + "\t🕳\nСтатус заявки: " + app[
                    8] + "\n🌐 Место положение:\n" + \
                          app[1] + "\n⏰ Дата и время:\n" + str(app[7]) + "\n"
                ans = types.InlineKeyboardMarkup()
                for i in range(len(status)):
                    button = types.InlineKeyboardButton(status[i], callback_data=f"edit_pothole{app_id}_{i}")
                    ans.add(button)

                bot.send_photo(call.message.chat.id, app[6], f"<b>{message}\nВыберите статус заявки 📝: </b>",
                               reply_markup=ans, parse_mode="html")

            if call.data.startswith("edit_pothole"):
                d = call.data.replace("edit_pothole", "")
                list = d.split("_")
                app_id = int(list[0])
                new_status = int(list[1])
                sql.update_status_ph(app_id, status[new_status])
                mark_from_db()
                message = f"<b>Новый статус заявки №{app_id}: {status[new_status]}</b>"
                bot.send_message(call.message.chat.id, message, parse_mode="html")

            if call.data == "профиль ямы":
                user_id = call.message.chat.id
                apps = sql.get_all_ph_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row_pothole = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_ph_profile_{app[0]}"))
                    else:
                        ans.row(*button_row_pothole)
                        c = 1
                        button_row_pothole = []
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_ph_profile_{app[0]}"))
                if button_row_pothole != []:
                    ans.row(*button_row_pothole)
                if button_row_pothole == []:
                    message = "<b>У Вас нет заявок на ямы! 🖇</b>"
                    bot.send_message(call.message.chat.id, f"<b>{message}</b>", reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Ваши отправленные заявки на ямы 🖇:\n{message}</b>",
                                     reply_markup=ans, parse_mode="html")

            if call.data.startswith("app_ph_profile_"):
                app_id = int(call.data.replace("app_ph_profile_", ""))
                app = sql.get_ph_by_id(app_id)
                s = "🔰<b>Заявка №</b>" + str(app[0]) + "\t🖇\nСтатус заявки: " + app[8] + "\n🌐 Место положение:\n" + \
                    app[1] + "\n⏰ Дата и время:\n" + str(app[7]) + "\n"
                bot.send_photo(call.message.chat.id, app[6], caption=f"<b>{s}</b>", parse_mode="html")

            if call.data == "профиль колодцы":
                user_id = call.message.chat.id
                apps = sql.get_all_well_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row_pothole = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_wl_profile_{app[0]}"))
                    else:
                        ans.row(*button_row_pothole)
                        c = 1
                        button_row_pothole = []
                        button_row_pothole.append(
                            types.InlineKeyboardButton(app[0], callback_data=f"app_wl_profile_{app[0]}"))
                if button_row_pothole != []:
                    ans.row(*button_row_pothole)
                if button_row_pothole == []:
                    message = "<b>У Вас нет заявок на открытые колодцы! 🕳</b>"
                    bot.send_message(call.message.chat.id, f"<b>{message}</b>", reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Ваши отправленные заявки на открытые колодцы 🕳:\n{message}</b>",
                                     reply_markup=ans, parse_mode="html")

            if call.data.startswith("app_wl_profile_"):
                app_id = int(call.data.replace("app_wl_profile_", ""))
                app = sql.get_well_by_id(app_id)
                s = "🔰<b>Заявка №</b>" + str(app[0]) + "\t🕳\nСтатус заявки: " + app[8] + "\n🌐 Место положение:\n" + \
                    app[1] + "\n⏰ Дата и время:\n" + str(app[7]) + "\n"
                bot.send_photo(call.message.chat.id, app[6], caption=f"<b>{s}</b>", parse_mode="html")

    except Exception as e:
        print(repr(e))

while True:
    try:

        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)

