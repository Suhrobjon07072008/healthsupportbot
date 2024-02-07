import telebot
from telebot.types import *
import sqlite3
import openai



bot = telebot.TeleBot("6788575244:AAE_L38LLKdQMgrLbSXZ2VPFq6pZy1zsiZ8")

def get_db_connection():
    return sqlite3.connect("users.db")





# Подготовка базы данных
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_users_table()





# Старт
@bot.message_handler(commands=['start'])
def start_command(message): 
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("🧑‍💻Регистрация"), telebot.types.KeyboardButton("🖐️Логин"))
    markup.add(telebot.types.KeyboardButton("📱Контакт"), telebot.types.KeyboardButton("💓Ближащие аптеки", request_location=True))
    bot.send_message(message.chat.id, "Здравствуйте! Я ChatGPT и health support бот. Что вы хотите сделать?", reply_markup=markup)




# Регистрация
@bot.message_handler(func=lambda message: message.text == "🧑‍💻Регистрация")
def registration_button(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте желаемое имя пользователя и пароль в формате: Логин:пароль")
    bot.register_next_step_handler(message, handle_registration)

def handle_registration(message):
    text = message.text.strip().split(':')
    if len(text) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, используйте формат: Логин:пароль")
        return

    username = text[0]
    password = text[1]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        bot.send_message(message.chat.id, "Пользователь с таким именем уже существует.")
    else:
        cursor.execute("INSERT INTO users (telegram_id, username, password) VALUES (?, ?, ?)",
                       (message.from_user.id, username, password))
        conn.commit()
        bot.send_message(message.chat.id, "Регистрация успешно завершена.")

    conn.close()





# Логин
@bot.message_handler(func=lambda message: message.text == "🖐️Логин")
def login_button(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваше имя пользователя и пароль в формате: Логин:пароль")
    bot.register_next_step_handler(message, handle_login)

def handle_login(message):
    text = message.text.strip().split(':')
    if len(text) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, используйте формат: Логин:пароль")
        return

    username = text[0]
    password = text[1]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        bot.send_message(message.chat.id, "Вход выполнен успешно.")
    else:
        bot.send_message(message.chat.id, "Неверное имя пользователя или пароль.")

    conn.close()





# Отправка локации
inmark= InlineKeyboardMarkup()
location_button1 = InlineKeyboardButton(text="Аптека НГМК", callback_data="ap1")
location_button2= InlineKeyboardButton(text="ХУМО Аптека", callback_data="ap2")
location_button3 = InlineKeyboardButton(text="Uzmed", callback_data="ap3")
location_button4 = InlineKeyboardButton(text="Grand Farm", callback_data="ap4")
location_button5 = InlineKeyboardButton(text="AJR Pharm", callback_data="ap5")
inmark.add(location_button1).add(location_button2).add(location_button3).add(location_button4).add(location_button5)

spisok = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Список аптек", callback_data="spisok"))


@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_location = message.location


    bot.send_message(message.chat.id, "Вот список ближащих аптек:", reply_markup=inmark)




# Аптеки
@bot.callback_query_handler(func=lambda call: call.data == "ap1")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.098647174837375, 65.37638762568365, reply_markup=spisok)  
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "ap2")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.10536832263608, 65.3815157842264, reply_markup=spisok)  
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "ap3")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.09047290714578, 65.37472127316738, reply_markup=spisok)  
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "ap4")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.08759797799526, 65.37798567508442, reply_markup=spisok)  
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "ap5")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.09338718733384, 65.38014578586724, reply_markup=spisok)  
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "spisok")
def send_location(call):
    bot.send_message(call.message.chat.id, "Вы вернулись в список аптек:", reply_markup=inmark)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    



# Контакты
@bot.message_handler(func=lambda message: message.text == "📱Контакт")
def login_button(message):
    bot.send_contact(message.chat.id, phone_number="+998975544455", first_name="Стомотология")
    bot.send_contact(message.chat.id, phone_number="+998959115522", first_name="Травматология")
    bot.send_contact(message.chat.id, phone_number="+998787770303", first_name="Хирургия")








# ChatGPT
openai.api_key="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"


@bot.message_handler()
def gpt(message):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"User: {message.text}\nBot: ",
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    ).choices[0].text

    if len(response)>4096:
        bot.send_message(message.chat.id, response[:4096]+"...")
        bot.send_message(message.chat.id, response[4096:])
    else:
        bot.send_message(message.chat.id, response)















bot.polling(none_stop=True)