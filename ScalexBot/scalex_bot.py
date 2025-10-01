import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

TOKEN = "8357720352:AAHU5LMw3eiNrZTDr6H5zshP4azmTURRH48"
bot = telebot.TeleBot(TOKEN)

# Твій Telegram ID для отримання заявок
ADMIN_ID = 8357843038  

user_data = {}

# --- Старт ---
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    text = (
        "👋 Привіт, я бот *Scalex*.\n\n"
        "Перед тим як заповнити заявку на співпрацю — "
        "підписка на Instagram засновника команди Scalex!\n\n"
        "Нові повідомлення скоро будуть!"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📲 Контакт", url="https://www.instagram.com/scalex_traffic_official?igsh=MWhtMnkzOGcycjRibw=="))
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)

    # Затримка 3 секунди
    time.sleep(3)
    kb2 = InlineKeyboardMarkup()
    kb2.add(InlineKeyboardButton("✅ Все готово?", callback_data="ready"))
    bot.send_message(chat_id, "Все готово?", reply_markup=kb2)

# --- Натискання "Так" ---
@bot.callback_query_handler(func=lambda call: call.data == "ready")
def ready_callback(call):
    chat_id = call.message.chat.id
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📩 Подати заявку", callback_data="apply"))
    bot.send_message(chat_id,
                     "👋 Доброго дня! Я ChatBot команди по арбітражу трафіка.\n"
                     "Якщо ви хочете приєднатися до нашої команди — залиште, будь ласка, заявку.",
                     reply_markup=kb)

# --- Подати заявку ---
@bot.callback_query_handler(func=lambda call: call.data == "apply")
def apply_callback(call):
    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, "✍️ Дякуємо за ваш інтерес до нашої команди! Вкажіть ваше ім'я:")
    bot.register_next_step_handler(msg, get_name)

# --- Отримання імені ---
def get_name(message):
    user_id = message.chat.id
    user_data[user_id] = {"name": message.text}
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Так", callback_data="exp_yes"))
    kb.add(InlineKeyboardButton("❌ Ні", callback_data="exp_no"))
    bot.send_message(user_id, "💼 Досвід є?", reply_markup=kb)

# --- Отримання досвіду ---
@bot.callback_query_handler(func=lambda call: call.data in ["exp_yes", "exp_no"])
def experience_callback(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    user_data[user_id]["experience"] = "Так" if call.data == "exp_yes" else "Ні"

    # Запит контакту
    msg = bot.send_message(user_id, "📲 Вкажіть свій Telegram або телефон для зв’язку:")
    bot.register_next_step_handler(msg, get_contact)

# --- Отримання контакту ---
def get_contact(message):
    user_id = message.chat.id
    user_data[user_id]["contact"] = message.text
    username = f"@{message.from_user.username}" if message.from_user.username else "немає"

    # Надсилаємо адміну
    application = (
        "📨 Нова заявка!\n\n"
        f"👤 Ім’я: {user_data[user_id]['name']}\n"
        f"💼 Досвід: {user_data[user_id]['experience']}\n"
        f"📲 Контакт: {user_data[user_id]['contact']}\n"
        f"🆔 Telegram: {username}\n"
        f"ID: {message.from_user.id}"
    )
    bot.send_message(ADMIN_ID, application)

    # Відповідь користувачу
    bot.send_message(user_id, "✅ Дякуємо за вашу заявку! Найближчим часом з вами зв’яжеться адміністратор.")

# --- Запуск бота ---
bot.infinity_polling()