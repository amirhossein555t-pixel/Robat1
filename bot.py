import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = "8778878221:AAEZcgWZuJMgCKA3NGC4tDf_RGbUh6tvwtI"

# سه کانال عضویت اجباری
CHANNELS = [
    "@AKVPN001",
    "@Hezb7Hitlerion",
    "@CHANNEL_3"
]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# لیست فیلم‌ها
FILMS = {
    "film1": "BAACAgQAAxkBAANTah2YB-skzr-05pMuHaT_Qijh-s8AAkAVAAIt2GlQNbCet5XRhHU7BA",
    "film2": "FILE_ID_FILM_2",
    "film3": "FILE_ID_FILM_3"
}

# ذخیره فیلم انتخاب‌شده برای هر کاربر
user_selected_film = {}

def membership_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 عضویت کانال 1", url="https://t.me/AKVPN001")
    kb.button(text="📢 عضویت کانال 2", url="https://t.me/.Hezb7Hitlerion")
    kb.button(text="📢 عضویت کانال 3", url="https://t.me/CHANNEL_3")
    kb.button(text="🟢 عضو شدم", callback_data="check_join")
    kb.adjust(1)
    return kb.as_markup()

async def check_all_channels(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True

@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()

    film_key = args[1] if len(args) > 1 else None

    # ذخیره فیلم انتخاب‌شده
    if film_key in FILMS:
        user_selected_film[user_id] = film_key

    # چک عضویت
    if not await check_all_channels(user_id):
        await message.answer("⚠️ برای دریافت فیلم باید در هر ۳ کانال عضو شوید 👇", reply_markup=membership_keyboard())
        return

    # ارسال فیلم
    if film_key in FILMS:
        await message.answer("🎬 در حال ارسال فیلم…")
        await bot.send_video(chat_id=message.chat.id, video=FILMS[film_key])
    else:
        await message.answer("❌ لینک فیلم اشتباهه یا فیلمی انتخاب نشده")

@dp.callback_query(lambda c: c.data == "check_join")
async def check_join_button(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if not await check_all_channels(user_id):
        await callback.answer("هنوز عضو هر ۳ کانال نشدی!", show_alert=True)
        return

    film_key = user_selected_film.get(user_id)

    if film_key:
        await callback.message.answer("✔️ عضویت تایید شد\n🎬 در حال ارسال فیلم…")
        await bot.send_video(chat_id=callback.message.chat.id, video=FILMS[film_key])
    else:
        await callback.message.answer("❌ فیلمی انتخاب نشده!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())