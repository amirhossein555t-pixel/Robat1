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

# توکن جدیدت رو اینجا بذار
TOKEN = "8778878221:AAEZcgWZuJMgCKA3NGC4tDf_RGbUh6tvwtI"

# کانال‌های عضویت اجباری
CHANNELS = [
    "@AKVPN001",
    "@Hezb7Hitlerion",          # فقط یوزرنیم تلگرام
    "@filmsoperzirnevis7"   # ← امیر اینجا کانال چهارم
]

# فیلم‌ها (۱۰ تا)
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
}

# شمارش بازدید
VIEWS = {key: 0 for key in FILMS.keys()}


def membership_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/Hezb7Hitlerion")],
        [InlineKeyboardButton("📢 عضویت در کانال 3", url="https://t.me/filmsoperzirnevis7")],
        [InlineKeyboardButton("🟢 عضو شدم", callback_data="check_join")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def check_membership(user_id, context):
    for ch in CHANNELS:
        if "CHANNEL_" in ch:
            continue  # کانال خالی هنوز اضافه نشده
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True


async def send_and_delete(context, chat_id, warn_id, video_id):
    await asyncio.sleep(20)
    try:
        await context.bot.delete_message(chat_id, video_id)
    except:
        pass
    try:
        await context.bot.delete_message(chat_id, warn_id)
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

    context.user_data["requested_film"] = film_key

    if not await check_membership(user_id, context):
        msg = await update.message.reply_text(
            "⚠️ برای دریافت فیلم باید عضو کانال‌ها بشی:",
            reply_markup=membership_keyboard(),
        )
        context.user_data["join_msg_id"] = msg.message_id
        return

    await send_film(update, context, film_key)


async def check_join_button(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if not await check_membership(user_id, context):
        await query.answer("❌ هنوز عضو نشدی!", show_alert=True)
        return

    await query.answer("✔️ عضویت تایید شد")

    # پاک کردن پیام عضویت اجباری
    join_msg_id = context.user_data.get("join_msg_id")
    if join_msg_id:
        try:
            await context.bot.delete_message(query.message.chat_id, join_msg_id)
        except:
            pass

    # پاک کردن خود پیام دکمه‌ها
    try:
        await query.message.delete()
    except:
        pass

    film_key = context.user_data.get("requested_film")
    await send_film(update, context, film_key, from_callback=True)


async def get_file_id(update, context):
    if update.message.video:
        await update.message.reply_text(f"🎬 File_ID:\n{update.message.video.file_id}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    for i in range(1, 11):
        app.add_handler(CommandHandler(f"film{i}", lambda u, c, x=i: start(u, c)))

    app.add_handler(CallbackQueryHandler(check_join_button))
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))

    print("Bot started…")
    app.run_polling()


if __name__ == "__main__":
    main()
