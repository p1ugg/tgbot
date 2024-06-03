import logging
import sys
from os import getenv
from random import randint

import dotenv
import telebot
from telebot import types

import Database

dotenv.load_dotenv()

TOKEN = getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

kb_start = types.InlineKeyboardMarkup()
kb_start.add(types.InlineKeyboardButton(
    text='Подписаться',
    url='https://t.me/laslaldlsala')
)
kb_start.add(types.InlineKeyboardButton(
    text='Проверить',
    callback_data='check')
)

def is_user_subscribed(user_id):
    try:
        member_status = bot.get_chat_member(chat_id='@laslaldlsala', user_id=user_id)
        return member_status.status != "left"
    except Exception as e:
        logging.error(f"Ошибка при проверке участия пользователя в канале: {e}")
        return False


@bot.message_handler(commands=['start'])
def command_start_handler(message):
    if not Database.check_user_in_db(str(message.from_user.id)):
        Database.add_user(str(message.from_user.id), message.from_user.full_name, '')
        if not Database.has_referrer(message.from_user.id):
            referrer = None

            if " " in message.text:
                referrer_candidate = message.text.split()[1]
                try:
                    referrer_candidate = int(referrer_candidate)

                    if message.from_user.id != referrer_candidate and str(referrer_candidate) in Database.get_all_users():
                        referer = referrer_candidate
                        Database.add_inv_ref(message.from_user.id, referer)
                        Database.update_balance(str(message.from_user.id), 100)
                        Database.update_balance(str(referrer_candidate), 200)

                except ValueError:
                    pass

        if is_user_subscribed(message.from_user.id):
            bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!\nДля начала выполни условия", reply_markup=kb_start)
        else:
            bot.send_message(message.chat.id, "Подпишитесь на канал @laslaldlsala", reply_markup=kb_start)
    else:
        bot.send_message(message.chat.id, f"С возвращением, {message.from_user.full_name}!\nДля проверки подписки нажми 'Проверить'", reply_markup=kb_start)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_subscribe(callback):
    if is_user_subscribed(callback.message.chat.id):
        try:
            bot.answer_callback_query(callback.id, "Вы являетесь участником канала ☑️")
            bot.send_message(callback.message.chat.id, text=f"ℹ️ Вы были приглашены пользователем {str(Database.get_name(callback.message.chat.id))}")

        except Exception as e:
            logging.error(f"Ошибка при проверке участия пользователя в канале: {e}")
            bot.answer_callback_query(callback.id, "Ошибка при проверке участия пользователя в канале!")
    else:
        bot.answer_callback_query(callback.id, "Подпишитесь на канал @laslaldlsala")




@bot.message_handler(commands=['referrals'])
def cmd_refferal(message):
    if is_user_subscribed(message.chat.id):
        ref_count = Database.get_referrals_count(message.chat.id)
        bot.send_message(message.chat.id, f"Кол-во рефов - {ref_count}.\nВаша реф ссылка - https://t.me/cerebrrrrrrr_test_bot?start={message.chat.id}")
        if ref_count >= 2:
            bot.send_message(message.chat.id, text=f"Ваши рефералы:\n{Database.get_referrals_names(str(message.chat.id))}")
    else:
        bot.send_message(message.chat.id, "Для использования бота подпишитесь на канал", reply_markup=kb_start)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot.polling(none_stop=True)
