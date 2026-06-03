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
PRIVATE_GROUP_ID = -1002295085920

# -------------------------
# 20 فیلم قبلی + 30 فیلم جدید (خالی)
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

    # 30 فیلم جدید خالی
    **{f"film{i}": "" for i in range(21, 51)}**
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


# -------------------------
# ارسال فیلم + حذف بعد ۲۰ ثانیه
# -------------------------
async def send_and_delete(context, chat_id, warn_id, video_id):
    await asyncio.sleep(20)
    for msg in [warn_id, video_id]:
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


# -------------------------
# استارت
# ---------------- update.effective update.effective_user.id

    VIEWS_user.id

    VIEWS[film_key] += 1

    target = update.callback_query.message if from_callback else update.message

    await target.reply_text(f"👁 این فیلم تا الان {VIEWS[film_key[film_key] += 1

    target = update]} بار دیده شده.")
.callback_query.message    warn = await target.reply_text if from_callback else update.message

    await target("⚠️ این فیلم ۲۰.reply_text(f"👁 این فیلم تا الان {VIEWS[film_key]} بار دیده شده.")
    warn = await target.reply_text ثانیه دیگه پاک میشه.")
    video = await context.bot.send_video(chat("⚠️ این فیلم ۲۰ ثانیه دیگه پاک میشه.")
    video = await context.bot.send_video(chat_id=user_id, video=FILMS[film_key])

    context.application.create_task(
       _id=user_id, video send_and_delete(context, user_id, warn.message_id, video.message_id)
    )


# -------------------------
# استارت
# -------------------------
async def start(update, context):
    user_id ==FILMS[film_key])

    context.application.create_task(
        send_and_delete(context, user_id update.effective, warn.message_id, video.message_id_user.id
    args)
    )


# ---------------- = context.args
    film_key = args---------
# استارت[0] if args else None

    if film
# -------------------------
async def start(update, context_key not in FILMS:
        await update.message.reply_text):
    user_id =("❌ لینک فیلم اشت update.effective_user.id
    argsباه است.")
        return

    context = context.args
.user_data["requested_film"] = film_key    film_key = args

    if not await[0] if args else check_membership None

    if film_key not in FILMS:
        await update(user_id, context.message.reply_text):
        msg =("❌ لینک فیلم اشت await update.message.reply_text(
           باه است.")
        return

    context "⚠️ برای دریافت فیلم باید عضو کانال‌ها و گروه بشی.user_data["requested_film"] = film_key

    if not await check_membership:",
            reply(user_id, context_markup=membership):
        msg = await update.message.reply_text(
           _keyboard(),
        "⚠️ برای دریافت )
        context فیلم باید عضو کان.user_data["join_msg_id"] = msg.message_id
        return

    await send_film(update, context, film_key)


# -------------------------
# دکمه «عضو شدم»
# -------------------------
async defال‌ها و گروه بشی check_join_button:",
            reply_markup=membership_keyboard(),
        )
        context.user_data["join_msg_id"] = msg.message_id
        return(update, context

    await send_film(update, context):
    query = update.callback_query
, film_key)


# ----------------    user_id = query---------
# دکمه.from_user.id

    if not await check_membership(user_id, context):
        «عضو شدم»
# ---------------- await query.answer---------
async def check_join_button("❌ هنوز عضو نشدی(update, context!", show_alert=True):
    query = update.callback_query
    user_id = query)
        return

    await query.answer("✔️ عضویت تایید شد")

   .from_user.id

    join_msg_id = context.user_data.get(" if not await check_membership(userjoin_msg_id")
   _id, context):
        await query.answer if join_msg_id:
        try:
           ("❌ هنوز عضو نشدی!", show_alert=True await context.bot.delete_message(query.message.chat_id)
        return, join_msg_id)
        except:
           

    await query pass

    try:
.answer("✔️ عضویت        await query تایید شد")

   .message.delete()
    except:
        join_msg_id = context.user_data.get("join_msg_id")
    pass

    film_key if join_msg_id:
 = context.user_data.get("requested_film")
    await send        try:
            await context.bot_film(update, context.delete_message(query.message.chat_id, join_msg_id)
        except:
           , film_key, from pass

    try:
_callback=True)


# -------------------------
# آمار        await query
# -------------------------
async def stats(update, context.message.delete()
):
    text = "📊    except:
        pass

    film_key آمار کل بازدیدها = context.user_data:\n\n"
    for key.get("requested_f, value in VIEWSilm")
    await send.items():
        text += f"{key}: {value} بازدید\n_film(update, context"
    await update, film_key, from.message.reply_text_callback=True)


(text)


# -------------------------
# گرفتن# -------------------------
# آمار
# ---------------- file_id
# -------------------------
async def---------
async def get_file_id(update, context):
    if update.message.video stats(update, context):
    text = "📊 آمار کل بازدیدها:
        await update.message.reply_text(f"🎬 File_ID:\n:\n\n"
    for key, value in VIEWS{update.message.video.file_id}")


# ----------------.items():
        text += f"{key}:---------
# اجرای ربات
# ---------------- {value} بازدید\n"
    await update---------
def main.message.reply_text():
    app = ApplicationBuilder().token(T(text)


# -------------------------
# گرفتنOKEN).build()

    app.add_handler file_id
# ----------------(CommandHandler("---------
async defstart", start))
 get_file_id(update    app.add_handler, context):
    if update.message.video:
        await update(CommandHandler("stats", stats))

    # 50 فیلم
    for i in range(1, 51):
        def make_handler(x):
.message.reply_text(f"🎬 File_ID:\n            return lambda update, context{update.message.video.file_id}")


# -------------------------
# اجرای ربات
# -------------------------
def main: start(update, context)
        app.add_handler(Command():
    app = ApplicationHandler(f"film{iBuilder().token(TOKEN).build()

   }", make_handler(i)))

    app.add_handler(Callback app.add_handler(CommandHandler("start", start))
    app.add_handlerQueryHandler(check(CommandHandler("stats", stats))

    # 50 فیلم
   _join_button))
    for i in range(1 app.add_handler, 51):
        def make_handler(x):
(MessageHandler(filters            return.VIDEO, get_file lambda update, context: start(update, context)
        app.add_id))

    print_handler(CommandHandler(f"film{i}", make_handler("Bot started…")
(i)))

    app.add    app.run_poll_handler(Callbacking()


if __name__ == "__main__":
QueryHandler(check    main()
