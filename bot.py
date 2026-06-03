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
    "@filmsoperzirnevis7",
    "@sexsazad001"
]

# -------------------------
# 20 FILMS
# -------------------------
FILMS = {
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
}

# شمارش بازدید
VIEWS = {key: 0 for key in FILMS.keys()}


def membership_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/Hezb7Hitlerion")],
        [InlineKeyboardButton("📢 عضویت در کانال 3", url="https://t.me/filmsoperzirnevis7")],
        [InlineKeyboardButton("📢 عضویت در کانال 4", url="https://t.me/sexsazad001")],
        [InlineKeyboardButton("🟢 عضو شدم", callback_data="check_join")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def check_membership(user_id, context):
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True


async def send_and_delete(context, chat_id, warn_id, video_id):
    await asyncio.sleep(20)
    for msg in [video_id, warn_id]:
        try:
            await context.bot.delete_message(chat_id, msg)
        except:
            pass


async def send_film(update, context, film_key, from_callback=False):
    user_id = update.effective_user.id

    VIEWS[film_key] += 1

    target = update.callback_query.message if from_callback else update.message

    await target.reply_text(f"👁 این فیلم تا الان {VIEWS[film_key]} بار دیده شده.")
    warn = await target.reply_text("⚠️ این فیلم ۲۰ ثانیه دیگه پاک میشه.")
    video = await context.bot.send_video(chat_id=user_id, video=FILMS[film_key])

    context.application.create_task(
        send_and_delete(context, user_id, warn.message_id, video.message_id)
    )


async def start(update, context):
    user_id = update.effective_user.id
    args = context.args
    film_key = args[0] if args else None

    if film_key not in FILMS:
        await update.message.reply_text("❌ لینک فیلم اشتباه است.")
        return

    context.user_data["requested_film"] = film_key

    if not await check_membership(user_id, context):
        msg = await update.message.reply_text(
            "⚠️ برای دریافت فیلم باید عضو کانال‌ها بشی:",
            reply_markup=membership_keyboard(),
        )
        context.user_data["join_msg_id"] = msg.message_id
        return

    await send_film(update, context, film_key)


# نسخه ضد گیر کردن
async def check_join_button(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if not await check_membership(user_id, context):
        await query.answer("❌ هنوز عضو نشدی!", show_alert=True)
        return

    await query.answer("✔️ عضویت تایید شد")

    try:
        await query.message.delete()
    except:
        pass

    join_msg_id = context.user_data.get("join_msg_id")
    if join_msg_id:
        try:
            await context.bot.delete_message(query.message.chat_id, join_msg_id)
        except:
            pass

    # گرفتن فیلم از context
    film_key = context.user_data.get("requested_film")

    # اگر context خالی بود → از متن start استخراج کن
    if not film_key:
        try:
            text = query.message.text
            if "/start" in text:
                film_key = text.replace("/start", "").strip()
        except:
            pass

    if not film_key:
        await query.message.reply_text("❌ خطا: فیلم پیدا نشد. دوباره لینک فیلم رو بزن.")
        return

    await send_film(update, context, film_key, from_callback=True)


async def stats(update, context):
    text = "📊 آمار کل بازدیدها:\n\n"
    for key, value in VIEWS.items():
        text += f"{key}: {value} بازدید\n"
    await update.message.reply_text(text)


async def get_file_id(update, context):
    if update.message.video:
        await update.message.reply_text(f"🎬 File_ID:\n{update.message.video.file_id}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    for i in range(1, 21):
        def make_handler(x):
            return lambda update, context: start(update, context)
        app.add_handler(CommandHandler(f"film{i}", make_handler(i)))

    app.add_handler(CallbackQueryHandler(check_join_button))
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))

    print("Bot started…")
    app.run_polling()


if __name__ == "__main__":
    main()
