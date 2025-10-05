import telebot
from telebot import types
import datetime
import json
import os

TOKEN = "8369546185:AAEORmtlgrhIlRK7njn27DjjGO-v59IgQAw"
bot = telebot.TeleBot(TOKEN)

# بيانات الرحلات مع الشرح باللغات الثلاثة
TRIPS = {
    1: {
        "name_ar": "القاهرة يوم واحد",
        "name_ru": "Каир 1 день",
        "name_en": "Cairo 1 Day",
        "price": 50,
        "description_ar": "جولة شاملة لأهم المعالم التاريخية في القاهرة.",
        "description_ru": "Всесторонний тур по главным историческим достопримечательностям Каира.",
        "description_en": "Comprehensive tour of Cairo's main historical landmarks."
    },
    2: {
        "name_ar": "الأقصر يوم واحد ملكات",
        "name_ru": "Луксор: Царицы",
        "name_en": "Luxor: Queens",
        "price": 50,
        "description_ar": "استكشاف وادي الملكات مع وسائل نقل مريحة.",
        "description_ru": "Исследование Долины Царей с удобным транспортом.",
        "description_en": "Exploring the Valley of the Queens with comfortable transportation."
    },
    3: {
        "name_ar": "الأقصر يوم واحد ملوك",
        "name_ru": "Луксор: Цари",
        "name_en": "Luxor: Kings",
        "price": 65,
        "description_ar": "رحلة مميزة في وادي الملوك مع شرح مرشد سياحي.",
        "description_ru": "Уникальная экскурсия по Долине Царей с гидом.",
        "description_en": "Unique tour of the Valley of the Kings with a guide."
    },
    4: {
        "name_ar": "الأقصر دندرة",
        "name_ru": "Луксор: Дендеры",
        "name_en": "Luxor: Dendera",
        "price": 75,
        "description_ar": "رحلة لاستكشاف معبد دندرة الأثري وجماله الخلاب.",
        "description_ru": "Экскурсия к древнему храму Дендера.",
        "description_en": "Trip to explore the ancient Temple of Dendera."
    },
    5: {
        "name_ar": "القاهرة - الإسكندرية",
        "name_ru": "Каир-Александрия",
        "name_en": "Cairo - Alexandria",
        "price": 140,
        "description_ar": "جولة ممتعة بين القاهرة والإسكندرية تشمل متاحف ومعالم.",
        "description_ru": "Путешествие между Каиром и Александрией с посещением музеев и достопримечательностей.",
        "description_en": "Exciting tour between Cairo and Alexandria including museums and landmarks."
    },
    6: {
        "name_ar": "جزيرة الأورانج",
        "name_ru": "Оранжевый остров",
        "name_en": "Orange Island",
        "price": 25,
        "description_ar": "استرخاء على الجزيرة وسط جو طبيعي ومنعش.",
        "description_ru": "Отдых на острове среди природы и свежего воздуха.",
        "description_en": "Relaxing on the island in natural and refreshing atmosphere."
    },
    7: {
        "name_ar": "جزيرة هولا هولا",
        "name_ru": "Остров Хола Хола",
        "name_en": "Hola Hola Island",
        "price": 25,
        "description_ar": "عودة الاستجمام مع جلسات مساج وبوفيه مفتوح.",
        "description_ru": "Отдых с массажем и шведским столом.",
        "description_en": "Relaxation with massage sessions and open buffet."
    },
    8: {
        "name_ar": "دولفين هاوس",
        "name_ru": "Дом Дельфинов",
        "name_en": "Dolphin House",
        "price": 25,
        "description_ar": "مشاهدة الدلافين والتمتع بالعروض المثيرة.",
        "description_ru": "Наблюдайте за дельфинами и наслаждайтесь шоу.",
        "description_en": "Watch dolphins and enjoy amazing shows."
    },
    9: {
        "name_ar": "غطس",
        "name_ru": "Дайвинг",
        "name_en": "Diving",
        "price": 25,
        "description_ar": "تجربة غطس احترافية في البحر الأحمر.",
        "description_ru": "Профессиональный дайвинг в Красном море.",
        "description_en": "Professional diving experience in the Red Sea."
    },
    10: {
        "name_ar": "سي سكوب",
        "name_ru": "Си Скуб",
        "name_en": "Sea Scoob",
        "price": 15,
        "description_ar": "جولة بحرية مع غواصة شفافة لمراقبة البحار.",
        "description_ru": "Экскурсия на прозрачной подводной лодке.",
        "description_en": "Tour in transparent submarine to observe sea life."
    },
    11: {
        "name_ar": "جب سفاري",
        "name_ru": "Джип Сафари",
        "name_en": "Jeep Safari",
        "price": 20,
        "description_ar": "مغامرة بالدراجات الجبلية على الكثبان الرملية.",
        "description_ru": "Приключение на джипах по песчаным дюнам.",
        "description_en": "Adventure jeep safari on sand dunes."
    },
    12: {
        "name_ar": "موتو سفاري",
        "name_ru": "Мото Сафари",
        "name_en": "Moto Safari",
        "price": 20,
        "description_ar": "جولة بالدراجات النارية عبر الصحارى الرائعة.",
        "description_ru": "Поездка на мотоциклах по живописной пустыне.",
        "description_en": "Motorcycle tour through scenic deserts."
    },
    13: {
        "name_ar": "سوبر سفاري",
        "name_ru": "Супер Сафари",
        "name_en": "Super Safari",
        "price": 25,
        "description_ar": "رحلة سفاري متكاملة مع كافة الخدمات.",
        "description_ru": "Полное сафари с полным обслуживанием.",
        "description_en": "Complete safari trip with full services."
    },
    14: {
        "name_ar": "حمام تركي ومساج",
        "name_ru": "Турецкая баня и массаж",
        "name_en": "Turkish bath and massage",
        "price": 25,
        "description_ar": "جلسات حمام تركي ومساج مريحة للاسترخاء.",
        "description_ru": "Расслабляющие турецкие бани и массажи.",
        "description_en": "Relaxing Turkish bath and massage sessions."
    },
    15: {
        "name_ar": "جراند أكواريوم",
        "name_ru": "Гранд Аквариум",
        "name_en": "Grand Aquarium",
        "price": 40,
        "description_ar": "زيارة أكبر الأحواض المائية وأنواع الكائنات البحرية.",
        "description_ru": "Посещение крупнейших аквариумов и морских животных.",
        "description_en": "Visit the largest aquariums and marine creatures."
    }
}

# بيانات التواصل
CONTACTS = {
    "website": "www.aht-s.com",
    "facebook_account": "https://facebook.com/aht.tirp",
    "facebook_page": "https://facebook.com/aht.Trips",
    "instagram": "https://instagram.com/aht.trips",
    "telegram_channel": "https://t.me/AHT_Trips_Booking"
}

# الترحيب والاختيار اللغة
user_languages = {}

def send_welcome(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    bot.send_message(chat_id, "مرحبًا! الرجاء اختيار اللغة / Please select language / Пожалуйста, выберите язык:", reply_markup=markup)

def get_text_by_lang(data, lang):
    return data.get(lang, "")

@bot.message_handler(commands=['start'])
def start_handler(message):
    send_welcome(message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data in ["lang_ar", "lang_ru", "lang_en"])
def language_selection_handler(call):
    lang = call.data.split("_")[1]
    user_languages[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_main_menu(call.message.chat.id, lang)

def show_main_menu(chat_id, lang):
    lang_map = {
        "ar": {
            "title": "اختر فئة الرحلات:",
            "premium": "⭐ جولات مميزة",
            "historical": "🏛️ رحلات تاريخية",
            "adventure": "🎯 مغامرات",
            "contact": "📞 تواصل معنا",
            "change_lang": "🔄 تغيير اللغة"
        },
        "ru": {
            "title": "Выберите категорию тура:",
            "premium": "⭐ Премиум туры",
            "historical": "🏛️ Исторические туры",
            "adventure": "🎯 Приключения",
            "contact": "📞 Связаться с нами",
            "change_lang": "🔄 Изменить язык"
        },
        "en": {
            "title": "Choose tour category:",
            "premium": "⭐ Premium Tours",
            "historical": "🏛️ Historical Tours",
            "adventure": "🎯 Adventures",
            "contact": "📞 Contact Us",
            "change_lang": "🔄 Change Language"
        }
    }
    buttons = [
        lang_map[lang]["premium"],
        lang_map[lang]["historical"],
        lang_map[lang]["adventure"],
        lang_map[lang]["contact"],
        lang_map[lang]["change_lang"]
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    bot.send_message(chat_id, lang_map[lang]["title"], reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def main_menu_handler(message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "ar")
    text = message.text

    lang_map = {
        "premium": {
            "ar": "⭐ جولات مميزة",
            "ru": "⭐ Премиум туры",
            "en": "⭐ Premium Tours"
        },
        "historical": {
            "ar": "🏛️ رحلات تاريخية",
            "ru": "🏛️ Исторические туры",
            "en": "🏛️ Historical Tours"
        },
        "adventure": {
            "ar": "🎯 مغامرات",
            "ru": "🎯 Приключения",
            "en": "🎯 Adventures"
        },
        "contact": {
            "ar": "📞 تواصل معنا",
            "ru": "📞 Связаться с нами",
            "en": "📞 Contact Us"
        },
        "change_lang": {
            "ar": "🔄 تغيير اللغة",
            "ru": "🔄 Изменить язык",
            "en": "🔄 Change Language"
        }
    }

    if text == lang_map["premium"][lang]:
        show_tours(message.chat.id, "premium", lang)
    elif text == lang_map["historical"][lang]:
        show_tours(message.chat.id, "historical", lang)
    elif text == lang_map["adventure"][lang]:
        show_tours(message.chat.id, "adventure", lang)
    elif text == lang_map["contact"][lang]:
        show_contacts(message.chat.id, lang)
    elif text == lang_map["change_lang"][lang]:
        send_welcome(message.chat.id)
    else:
        bot.send_message(message.chat.id, {"ar": "اختر خيارًا من القائمة.", "ru": "Выберите вариант из меню.", "en": "Please choose an option from the menu."}[lang])

def show_tours(chat_id, category, lang):
    cat_map = {
        "premium": [1, 2],
        "historical": [3, 4, 5],
        "adventure": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    }
    tour_ids = cat_map.get(category, [])
    text = ""
    for tid in tour_ids:
        trip = TRIPS[tid]
        name = trip[f"name_{lang}"]
        price = trip["price"]
        description = trip[f"description_{lang}"]
        text += f"📝 *{name}* - ${price}
{description}

"
    bot.send_message(chat_id, text, parse_mode="Markdown")

def show_contacts(chat_id, lang):
    texts = {
        "ar": f"""
📞 تواصل معنا:

🌐 الموقع الرسمي: {CONTACTS['website']}
📘 فيسبوك حساب: {CONTACTS['facebook_account']}
📘 فيسبوك صفحة: {CONTACTS['facebook_page']}
📸 إنستغرام: {CONTACTS['instagram']}
📲 قناة التيليجرام: {CONTACTS['telegram_channel']}
""",
        "ru": f"""
📞 Связаться с нами:

🌐 Официальный сайт: {CONTACTS['website']}
📘 Facebook аккаунт: {CONTACTS['facebook_account']}
📘 Facebook страница: {CONTACTS['facebook_page']}
📸 Instagram: {CONTACTS['instagram']}
📲 Телеграм канал: {CONTACTS['telegram_channel']}
""",
        "en": f"""
📞 Contact us:

🌐 Official Website: {CONTACTS['website']}
📘 Facebook Account: {CONTACTS['facebook_account']}
📘 Facebook Page: {CONTACTS['facebook_page']}
📸 Instagram: {CONTACTS['instagram']}
📲 Telegram Channel: {CONTACTS['telegram_channel']}
"""
    }
    bot.send_message(chat_id, texts[lang])

print("🛠️ بوت الحجوزات المتعدد اللغات جاهز للعمل!")

bot.polling()