from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# توکن جدیدت رو اینجا بذار
TOKEN = "YOUR_BOT_TOKEN"

# کانال‌های عضویت اجباری
CHANNELS = [
    "@AKVPN001",
    "@Hezb7Hitlerion"   # فقط یوزرنیم تلگرام است
]

# فیلم‌ها (بعداً File_ID را جایگزین کن)
FILMS = {
    "film1": "FILE_ID_FILM_1",
    "film2": "FILE_ID_FILM_2",
    "film3": "FILE_ID_FILM_3"
}

# دکمه‌های پهن عضویت
def membership_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در کانال 1", url="https://t.me/AKVPN001")],
        [InlineKeyboardButton("📢 عضویت در کانال 2", url="https://t.me/Hezb7Hitlerion")],
        [InlineKeyboardButton("🟢 عضو شدم", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(keyboard)

# چک عضویت
async def check_membership(user_id, context: ContextTypes.DEFAULT_TYPE):
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True

# /start + لینک اختصاصی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    film_key = args[0] if args else None

    # چک عضویت
    if not await check_membership(user_id, context):
        await update.message.reply_text(
            "⚠️ برای دریافت فیلم باید عضو کانال‌ها بشی:",
            reply_markup=membership_keyboard()
        )
        return

    # ارسال فیلم
    if film_key in FILMS:
        await update.message.reply_text("🎬 در حال ارسال فیلم…")
        await context.bot.send_video(chat_id=user_id, video=FILMS[film_key])
    else:
        await update.message.reply_text("هیچ فیلمی انتخاب نشده!")

# دکمه «عضو شدم»
async def check_join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if not await check_membership(user_id, context):
        await query.answer("❌ هنوز عضو نشدی!", show_alert=True)
        return

    await query.answer("✔️ عضویت تایید شد")
    await query.message.reply_text("الان دوباره روی لینک فیلم بزن 🌟")

# دستورات مستقیم
async def film1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def film2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def film3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# گرفتن File_ID از ویدیو
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"🎬 File_ID:\n{file_id}")
    else:
        await update.message.reply_text("⚠️ فقط ویدیو بفرست تا File_ID بدم.")

# اجرای ربات
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("film1", film1))
    app.add_handler(CommandHandler("film2", film2))
    app.add_handler(CommandHandler("film3", film3))
    app.add_handler(CallbackQueryHandler(check_join_button))
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))

    print("Bot started…")
    app.run_polling()

if __name__ == "__main__":
    main()
