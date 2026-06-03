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

TOKEN = "8778878221:AAEZcgWZuJMgCKA3NGC4tDf_RGbUh6tvwtI"

CHANNELS = [
    "@AKVPN001",
    "@Hezb7Hitlerion",
    "@filmsoperzirnevis7",
    "@sexsazad001"
]

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

VIEWS = {key: 0 for key in FILMS.keys()}


def membership_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/Hezb7Hitlerion")],
        [InlineKeyboardButton("📢 عضویت در کانال 3", url="https://t.me/filmsoperzirnevis7")],
        [InlineKeyboardButton("📢 عضویت در کانال 4", url="https://t.me/sexsazad001")],
        [InlineKeyboardButton("🟢 عضو شدم", callback_data="check_join")]
    ])


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


async def send_film_direct(update, context, film_key):
    user_id = update.effective_user.id
    VIEWS[film_key] += 1

    await update.effective_message.reply_text(f"👁 این فیلم تا الان {VIEWS[film_key]} بار دیده شده.")
    warn = await update.effective_message.reply_text("⚠️ این فیلم ۲۰ ثانیه دیگه پاک میشه.")
    video = await context.bot.send_video(chat_id=user_id, video=FILMS[film_key])

    context.application.create_task(
        send_and_delete(context, user_id, warn.message_id, video.message_id)
    )


async def start(update, context):
    args = context.args
    if not args:
        await update.message.reply_text("❌ لینک فیلم اشتباه است.")
        return

    film_key = args[0]

    if film_key not in FILMS:
        await update.message.reply_text("❌ فیلم پیدا نشد.")
        return

    update.user_data["film"] = film_key

    if not await check_membership(update.effective_user.id, context):
        await update.message.reply_text(
            "⚠️ برای دریافت فیلم باید عضو کانال‌ها بشی:",
            reply_markup=membership_keyboard()
        )
        return

    await send_film_direct(update, context, film_key)


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

    film_key = update.user_data.get("film")

    if not film_key:
        await query.message.reply_text("❌ خطا: فیلم پیدا نشد. دوباره لینک فیلم رو بزن.")
        return

    await send_film_direct(update, context, film_key)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join_button))

    print("Bot started…")
    app.run_polling()


if __name__ == "__main__":
    main()
