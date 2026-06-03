import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# توکن ربات
TOKEN = "8778878221:AAEZcgWZuJMgCKA3NGC4tDf_RGbUh6tvwtI"

# کانال‌های عضویت اجباری
CHANNELS = [
    "@AKVPN001",
    "@Hezb7Hitlerion",
    "@filmsoperzirnevis7"
]

# گروه پرایوت (اد اجباری)
PRIVATE_GROUP_LINK = "https://t.me/+giTXzRnwDmkxZjBk"
PRIVATE_GROUP_ID = -1002295085920   # آماده برای استفاده

# -------------------------
# 20 FILMS قبلی + 30 FILMS جدید (خالی)
# -------------------------
FILMS = {
    # 20 فیلم قبلی
    "film1": "BAACAgQAAxkBAAPEah6LOE_vcpDewjZPJIJzVYdy6yYAAmAXAAL0MvBSsPoIl8HMNCo7BA",
    "film2": "BAACAgQAAxkBAAPGah6LbKBL6YSsTzC0FQoXFXGqCKAAAmcXAALzxRhT5n24uZPupHQ7BA",
    "film3": "BAACAgQAAxkBAAPIah6LkiIcBlqEZN2vmDyNrTN1GvoAAswbAAJHoiBTbfarsn-1bu07BA",
    "film4": "BAACAgQAAxkBAAPKah6Lt4diawJSnwmedCI_k89zsEwAAuEcAALVPzhTVrtBqnlrZZA7BA",
    "film5": "BAACAgQAAxkBAAPMah6ME4-TNae25U6N21vjfX4Ydj4AAvcbAAKEbgABUPZUTvwaI25iOwQ",
    "film6": "BAACAgQAAxkBAAPOah6Pu79GEBxUM7fZWwqSwSh6NM4AAx4AArU2aVCWlZ7Up580mTsE",
    "film7": "BAACAgQAAxkBAAPQah6QDuxotcOWH8d6rOsRJx-Tm1cAApAbAAK4IfFQOT2mTu6Vi747BA",
    "film8": "BAACAgQAAxkBAAPSah6QNRMQlkEBu3D8okQgL0vYEtoAApEbAAK4IfFQNqk4rauoF_o7BA",
    "film9": "BAACAgQAAxkBAAPUah6QX8Rr4kSKp2tg5aD5xC1lJh0AAukZAAKtZAhRopyCes6bSEo7BA",
    "film10": "BAACAgQAAxkBAAPWah6QqbzbjbwyHJBKdzkjEhQutvgAArYYAALsoChRXUXgdQOa5TE7BA",

    "film11": "BAACAgQAAxkBAAIDMmoe9njXPpRX0pSc-9NnTKctWbM7AAK3GwACd7dJUavBDSB3l5OjOwQ",
    "film12": "BAACAgQAAxkBAAIDNGoe9qH7x6I0baX9JwqlE3z111zcAAK9GwACd7dJUZDEGLie5aqROwQ",
    "film13": "BAACAgQAAxkBAAIDNmoe9s-AzfK2ygsGIJTze20EIHyTAAJQGQACWVBZUcu43L2YWsAaOwQ",
    "film14": "BAACAgQAAxkBAAIDOGoe9utQk895m6KW17OLMc_AykimAALjGQACWVBZUfFmhe5JUDxaOwQ",
    "film15": "BAACAgQAAxkBAAIDOmoe9xBs-jqZdfeagmErInj5ESlrAAK2GwACx8lhUe3XkPsdKoqFOwQ",
    "film16": "BAACAgQAAxkBAAIDRGoe95XN-8xQF7i8WI5vBDJCl4iiAAL3GgACx8lpUX-9GlBESJkAATsE",
    "film17": "BAACAgQAAxkBAAIDRmoe98uTxzLMgx9JCwybw1nKN-nFAALUGwACx8lpUVhsSR-aFSksOwQ",
    "film18": "BAACAgQAAxkBAAIDSGoe9_VdtxCxzSA7Twc7DK8iNyK1AAILHAACx8lpUUlZTmfhColsOwQ",
    "film19": "BAACAgQAAxkBAAIDSmoe-BpqA7uQu9LsHzr5hDFKfGYbAAIbKAACOiaIUY-GKp6Q4VolOwQ",
    "film20": "BAACAgQAAxkBAAIDTWoe-EK3GHdeCnIf-pedexkQ2RUMAALRHAACDNmoUcRcFAj-mnELOwQ",

    # -------------------------
    # 30 فیلم جدید (خالی)
    # -------------------------
    "film21": "",
    "film22": "",
    "film23": "",
    "film24": "",
    "film25": "",
    "film26": "",
    "film27": "",
    "film28": "",
    "film29": "",
    "film30": "",
    "film31": "",
    "film32": "",
    "film33": "",
    "film34": "",
    "film35": "",
    "film36": "",
    "film37": "",
    "film38": "",
    "film39": "",
    "film40": "",
    "film41": "",
    "film42": "",
    "film43": "",
    "film44": "",
    "film45": "",
    "film46": "",
    "film47": "",
    "film48": "",
    "film49": "",
    "film50": "",
}

# شمارش بازدید
VIEWS = {key: 0 for key in FILMS.keys()}


# -------------------------
# چک عضویت کانال + گروه
# -------------------------
async def check_membership(user_id, context):
    # چک کانال‌ها
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False

    # چک گروه پرایوت
    try:
        member = await context.bot.get_chat_member(PRIVATE_GROUP_ID, user_id)
        if member.status == "left":
            return False
    except:
        return False

    return True


# -------------------------
# دکمه‌های عضویت
# -------------------------
def membership_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/Hezb7Hitlerion")],
        [InlineKeyboardButton("📢 عضویت در کانال 3", url="https://t.me/filmsoperzirnevis7")],
        [InlineKeyboardButton("👥 عضویت در گروه", url=PRIVATE_GROUP_LINK)],
        [InlineKeyboardButton("🟢 عضو شدم", callback_data="check_join")],
    ]
    return InlineKeyboardMarkup(keyboard)
