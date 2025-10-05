import telebot
from telebot import types
import json
import datetime
import os

TOKEN = "8369546185:AAEORmtlgrhIlRK7njn27DjjGO-v59IgQAw"
bot = telebot.TeleBot(TOKEN)

DB_FILE = "booking_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "bookings": [], "stats": {"total_bookings": 0, "active_users": 0}}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

TOURS = {
    "historical": [
        {"id": 1, "name_ar": "القاهرة يوم واحد", "price": 50, "duration_ar": "يوم واحد"},
        {"id": 2, "name_ar": "الاقصر يوم واحد ملكات", "price": 50, "duration_ar": "يوم واحد"},
        {"id": 3, "name_ar": "الاقصر يوم واحد ملوك", "price": 65, "duration_ar": "يوم واحد"},
        {"id": 4, "name_ar": "الاقصر دندره", "price": 75, "duration_ar": "يوم واحد"},
        {"id": 5, "name_ar": "القاهره اسكندريه", "price": 140, "duration_ar": "يومان"}
    ],
    "islands": [
        {"id": 6, "name_ar": "جزيرة الاورانج", "price": 25, "duration_ar": "نصف يوم"},
        {"id": 7, "name_ar": "جزيرة هولا هولا", "price": 25, "duration_ar": "نصف يوم"}
    ],
    "marine": [
        {"id": 8, "name_ar": "دولفين هاوس", "price": 25, "duration_ar": "نصف يوم"},
        {"id": 9, "name_ar": "غطس", "price": 25, "duration_ar": "نصف يوم"},
        {"id": 10, "name_ar": "سى سكوب", "price": 15, "duration_ar": "نصف يوم"}
    ],
    "safari": [
        {"id": 11, "name_ar": "جب سفاري", "price": 20, "duration_ar": "نصف يوم"},
        {"id": 12, "name_ar": "موتو سفاري", "price": 20, "duration_ar": "نصف يوم"},
        {"id": 13, "name_ar": "سوبر سفاري", "price": 25, "duration_ar": "نصف يوم"}
    ],
    "entertainment": [
        {"id": 14, "name_ar": "حمام تركي ومساج", "price": 25, "duration_ar": "ساعتان"},
        {"id": 15, "name_ar": "جراند اكواريوم", "price": 40, "duration_ar": "ساعتان"}
    ],
}

user_language = {}

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    db = load_db()
    if str(user_id) not in db["users"]:
        db["users"][str(user_id)] = {
            "join_date": datetime.datetime.now().isoformat(),
            "total_bookings": 0
        }
        db["stats"]["active_users"] = len(db["users"])
        save_db(db)
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    )
    bot.send_message(chat_id, "اختر لغتك / Choose your language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    lang = call.data.replace("lang_", "")
    user_language[call.from_user.id] = lang
    bot.answer_callback_query(call.id, "تم اختيار اللغة." if lang=="ar" else "Language selected.")
    show_main_menu(call.message.chat.id, lang)

def show_main_menu(chat_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = {
        "ar": ['🏛️ الرحلات التاريخية', '🏝️ جولات الجزر', '🐠 الجولات البحرية', '🚙 رحلات السفاري', '🎯 الترفيه والأنشطة'],
        "en": ['🏛️ Historical Tours', '🏝️ Island Tours', '🐠 Marine Tours', '🚙 Safari Trips', '🎯 Entertainment & Activities'],
        "ru": ['🏛️ Исторические туры', '🏝️ Островные туры', '🐠 Морские туры', '🚙 Сафари', '🎯 Развлечения и активности']
    }
    markup.add(*buttons.get(lang, buttons["ar"]))
    bot.send_message(chat_id, "اختر فئة الرحلات:" if lang=="ar" else "Choose a tour category:" if lang=="en" else "Выберите категорию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_category(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ar")
    text = message.text
    chat_id = message.chat.id
    
    categories = {
        "ar": {"الرحلات": "historical", "الجزر": "islands", "البحرية": "marine", "سفاري": "safari", "الترفيه": "entertainment"},
        "en": {"Historical": "historical", "Island": "islands", "Marine": "marine", "Safari": "safari", "Entertainment": "entertainment"},
        "ru": {"Исторические": "historical", "Остров": "islands", "Морские": "marine", "Сафари": "safari", "Развлечения": "entertainment"}
    }
    
    mapped_cat = None
    for k, v in categories.get(lang, {}).items():
        if k in text:
            mapped_cat = v
            break
    
    if mapped_cat:
        show_tours(chat_id, lang, mapped_cat)
    else:
        bot.send_message(chat_id, "اختر من القائمة فقط." if lang=="ar" else "Please choose from the menu." if lang=="en" else "Пожалуйста, выберите из меню.")

def show_tours(chat_id, lang, category):
    tours = TOURS.get(category, [])
    for tour in tours:
        text = f"*{tour['name_ar']}* - 💵 *${tour['price']}*\n⏳ المدة: {tour['duration_ar']}"
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("احجز الآن" if lang=="ar" else "Book Now" if lang=="en" else "Забронировать", callback_data=f"book_{tour['id']}")
        )
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def start_booking(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    tour_id = int(call.data.replace("book_", ""))
    lang = user_language.get(user_id, "ar")
    
    db = load_db()
    booking = {
        "user_id": user_id,
        "tour_id": tour_id,
        "booking_time": datetime.datetime.now().isoformat()
    }
    db["bookings"].append(booking)
    db["stats"]["total_bookings"] += 1
    if str(user_id) in db["users"]:
        db["users"][str(user_id)]["total_bookings"] += 1
    save_db(db)
    
    bot.answer_callback_query(call.id, "تم الحجز بنجاح!" if lang=="ar" else "Booking successful!" if lang=="en" else "Бронирование прошло успешно!")
    bot.send_message(chat_id, "شكراً لحجزك معنا!" if lang=="ar" else "Thank you for your booking!" if lang=="en" else "Спасибо за бронирование!")

if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.polling(none_stop=True)
