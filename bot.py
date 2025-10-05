import telebot
from telebot import types
import time

TOKEN = "8369546185:AAEORmtlgrhIlRK7njn27DjjGO-v59IgQAw"
bot = telebot.TeleBot(TOKEN)

bot.remove_webhook()
time.sleep(1)  # وقت قليل لتفعيل الإزالة

PROFESSIONAL_DATA = {
    "company": {
        "name_ar": "AHT Travel",
        "name_ru": "AHT Travel",
        "name_en": "AHT Travel",
        "phone": "+20 10303319293",
        "email": "booking@aht-s.com",
        "website": "www.aht-s.com",
        "address_ar": "الغردقة، مصر",
        "address_ru": "Хургада, Египет",
        "address_en": "Hurghada, Egypt"
    },
    "tours": [
        {"id": 1, "name_ar": "القاهرة يوم واحد", "name_ru": "Каир 1 день", "name_en": "Cairo 1 Day", "price": 50},
        {"id": 2, "name_ar": "الاقصر يوم واحد ملكات", "name_ru": "Луксор: Царицы", "name_en": "Luxor: Queens 1 Day", "price": 50},
        {"id": 3, "name_ar": "الاقصر يوم واحد ملوك", "name_ru": "Луксор: Цари", "name_en": "Luxor: Kings 1 Day", "price": 65},
        {"id": 4, "name_ar": "الاقصر دندره", "name_ru": "Дендера", "name_en": "Dendera Luxor", "price": 75},
        {"id": 5, "name_ar": "القاهرة اسكندريه", "name_ru": "Каир- Александрия", "name_en": "Cairo Alexandria", "price": 140},
        {"id": 6, "name_ar": "جزيرة الاورانج", "name_ru": "Оранжевый остров", "name_en": "Orange Island", "price": 25},
        {"id": 7, "name_ar": "جزيرة هولا هولا", "name_ru": "Остров Хула Хула", "name_en": "Hula Hula Island", "price": 25},
        {"id": 8, "name_ar": "دولفين هاوس", "name_ru": "Дом дельфинов", "name_en": "Dolphin House", "price": 25},
        {"id": 9, "name_ar": "غطس", "name_ru": "Дайвинг", "name_en": "Diving", "price": 25},
        {"id": 10, "name_ar": "سى سكوب", "name_ru": "Си Скоб", "name_en": "Sea Scoob", "price": 15},
        {"id": 11, "name_ar": "جب سفاري", "name_ru": "Горное сафари", "name_en": "Mountain Safari", "price": 20},
        {"id": 12, "name_ar": "موتو سفاري", "name_ru": "Мото сафари", "name_en": "Moto Safari", "price": 20},
        {"id": 13, "name_ar": "سوبر سفاري", "name_ru": "Супер сафари", "name_en": "Super Safari", "price": 25},
        {"id": 14, "name_ar": "حمام تركي ومساج", "name_ru": "Турецкая баня и массаж", "name_en": "Turkish Bath and Massage", "price": 25},
        {"id": 15, "name_ar": "جراند اكواريوم", "name_ru": "Гранд аквариум", "name_en": "Grand Aquarium", "price": 40}
    ]
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_data[user_id] = {"language": "ar"}

    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )

    welcome_text = ("🏝️ *AHT Travel - Booking Bot*\n\n"
                    "Please select your language / Пожалуйста, выберите язык / الرجاء اختيار اللغة:")
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    user_data[call.from_user.id] = {"language": lang}
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_tours(call.message.chat.id, lang)


def show_tours(chat_id, lang):
    text_lines = []
    tour_icon = "🎯"

    titles = {
        "ar": "قائمة الرحلات المتاحة:",
        "ru": "Список доступных туров:",
        "en": "Available Tours:"
    }

    for tour in PROFESSIONAL_DATA["tours"]:
        name = tour[f"name_{lang}"]
        price = tour["price"]
        # عرض الاسم والسعر مع الإيموجي
        text_lines.append(f"{tour_icon} *{name}* - 💰 {price}")

    text = f"*{titles[lang]}*\n\n" + "\n".join(text_lines)

    markup = types.InlineKeyboardMarkup(row_width=1)
    for tour in PROFESSIONAL_DATA["tours"]:
        name = tour[f"name_{lang}"]
        markup.add(types.InlineKeyboardButton(f"🔖 {name}", callback_data=f"book_{tour['id']}"))

    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def book_tour(call):
    tour_id = int(call.data.split("_")[1])
    lang = user_data.get(call.from_user.id, {}).get("language", "ar")

    tour = next((t for t in PROFESSIONAL_DATA["tours"] if t["id"] == tour_id), None)
    if not tour:
        bot.answer_callback_query(call.id, "Invalid selection.")
        return

    name = tour[f"name_{lang}"]
    price = tour["price"]
    contact = PROFESSIONAL_DATA["company"]["phone"]

    texts = {
        "ar": f"✨ *تم اختيار الجولة:* {name}\n💰 السعر: {price}\n📞 للحجز يرجى التواصل معنا: {contact}",
        "ru": f"✨ *Вы выбрали тур:* {name}\n💰 Цена: {price}\n📞 Для бронирования свяжитесь с нами: {contact}",
        "en": f"✨ *You selected tour:* {name}\n💰 Price: {price}\n📞 To book please contact us: {contact}"
    }

    bot.edit_message_text(texts[lang], call.message.chat.id, call.message.message_id, parse_mode='Markdown')


def main():
    while True:
        try:
            print("🟢 Bot is running...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"⚠️ Error occurred: {e}. Restarting in 10 seconds...")
            time.sleep(10)


if __name__ == '__main__':
    main()

