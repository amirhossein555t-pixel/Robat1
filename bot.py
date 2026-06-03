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

توکن ربات
TOKEN = "8778878221:AAEZcgWZuJMgCKA3NGC4tDf_RGbUh6tvwtI"

کانال‌های عضویت اجباری
CHANNELS = [
    "@AKVPN001",
    "@sexsazad001",
    "@filmsoperzirnevis7"
]

-------------------------

20 FILMS

-------------------------
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

    # جدیدها
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

شمارش بازدید
VIEWS = {key: 0 for key in FILMS.keys()}


def membership_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/sexsazad001")],
        [InlineKeyboardButton("📢 عضویت در کانال 3", url="https://t.me/filmsoperzirnevis7")],
        [InlineKeyboardButton("🟢 عضو شدم", callbackdata="checkjoin")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def checkmembership(userid, context):
    for ch in CHANNELS:
        try:
            member = await context.bot.getchatmember(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True


async def sendanddelete(context, chatid, warnid, video_id):
    await asyncio.sleep(20)
    for msg in [videoid, warnid]:
        try:
            await context.bot.deletemessage(chatid, msg)
        except:
            pass


async def sendfilm(update, context, filmkey, from_callback=False):
    userid = update.effectiveuser.id

    VIEWS[film_key] += 1

    target = update.callbackquery.message if fromcallback else update.message

    await target.replytext(f"👁 این فیلم تا الان {VIEWS[filmkey]} بار دیده شده.")
    warn = await target.reply_text("⚠️ این فیلم ۲۰ ثانیه دیگه پاک میشه.")
    video = await context.bot.sendvideo(chatid=userid, video=FILMS[filmkey])

    context.application.create_task(
        sendanddelete(context, userid, warn.messageid, video.message_id)
    )


async def start(update, context):
    userid = update.effectiveuser.id
    args = context.args
    film_key = args[0] if args else None

    if film_key not in FILMS:
        await update.message.reply_text("❌ لینک فیلم اشتباه است.")
        return

    context.userdata["requestedfilm"] = film_key

    if not await checkmembership(userid, context):
        msg = await update.message.reply_text(
            "⚠️ برای دریافت فیلم باید عضو کانال‌ها بشی:",
            replymarkup=membershipkeyboard(),
        )
        context.userdata["joinmsgid"] = msg.messageid
        return

    await sendfilm(update, context, filmkey)


async def checkjoinbutton(update, context):
    query = update.callback_query
    userid = query.fromuser.id

    if not await checkmembership(userid, context):
        await query.answer("❌ هنوز عضو نشدی!", show_alert=True)
        return

    await query.answer("✔️ عضویت تایید شد")

    joinmsgid = context.userdata.get("joinmsg_id")
    if joinmsgid:
        try:
            await context.bot.deletemessage(query.message.chatid, joinmsgid)
        except:
            pass

    try:
        await query.message.delete()
    except:
        pass

    filmkey = context.userdata.get("requested_film")
    await sendfilm(update, context, filmkey, from_callback=True)


async def stats(update, context):
    text = "📊 آمار کل بازدیدها:\n\n"
    for key, value in VIEWS.items():
        text += f"{key}: {value} بازدید\n"
    await update.message.reply_text(text)


async def getfileid(update, context):
    if update.message.video:
        await update.message.replytext(f"🎬 FileID:\n{update.message.video.file_id}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    # 20 فیلم
    for i in range(1, 21):
        def make_handler(x):
            return lambda update, context: start(update, context)
        app.addhandler(CommandHandler(f"film{i}", makehandler(i)))

    app.addhandler(CallbackQueryHandler(checkjoin_button))
    app.addhandler(MessageHandler(filters.VIDEO, getfile_id))

    print("Bot started…")
    app.run_polling()


if name == "main":
    main()
