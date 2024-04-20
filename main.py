import asyncio
import logging
import sys
from os import getenv
from pprint import pprint
from random import randint

import dotenv

from aiogram import Bot, Dispatcher, html, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher import router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text
from aiogram import F
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import Database

dotenv.load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router(name=__name__)

# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     user_id = message.from_user.id
#     referrer = None
#
#     # Проверяем наличие хоть какой-то дополнительной информации из ссылки
#     if " " in message.text:
#         referrer_candidate = message.text.split()[1]
#         print(referrer_candidate)
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!. You invited by {referrer_candidate}")

subscribed = False


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    global subscribed
    kb_start = InlineKeyboardBuilder()
    kb_start.add(InlineKeyboardButton(
        text='Подписаться',
        url='https://t.me/laslaldlsala')
    )
    kb_start.add(InlineKeyboardButton(
        text='Проверить',
        callback_data='link')
    )

    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\nДля начала выполни условия",
                         reply_markup=kb_start.as_markup())


@dp.callback_query(F.data == "link")
async def send_random_value(callback: types.CallbackQuery, bot: Bot):
    global subscribed

    try:
        member_status = await bot.get_chat_member(chat_id='@laslaldlsala', user_id=callback.message.chat.id)
        if member_status.status != 'left':
            await callback.answer("Вы являетесь участником канала ☑️")
            subscribed = True

            ## тут дописать кем он инвайтнут
        else:
            await callback.answer("Вы не являетесь участником канала ❌")
    except Exception as e:
        logging.error(f"Ошибка при проверке участия пользователя в канале: {e}")
        await callback.answer("Ошибка при проверке участия пользователя в канале!")
        # await callback.message.answer(res.status)


@dp.message(Command("referral"))
async def cmd_refferal(message: types.Message):
    global subscribed
    if not subscribed:
        await message.answer("Пожалуйста, подпишитесь на канал, чтобы продолжить использование бота.")
    else:
        ref_count = Database.get_referrals_count(message.chat.id)
        await message.answer(
            f"Кол-во рефов - {ref_count}.\nВаша реф ссылка - https://t.me/cerebrrrrrrr_test_bot?start={message.chat.id}")


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    global subscribed
    if not subscribed:
        await message.answer("Пожалуйста, подпишитесь на канал, чтобы продолжить использование бота.")
    else:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Нажми меня",
            callback_data="random_value")
        )
        await message.answer(
            "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
            reply_markup=builder.as_markup()
        )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
