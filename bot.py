from aiogram import Bot, types
from isort import Config
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from app.handlers.create_event import register_handlers_create_event
from app.handlers.common import register_handlers_common
from app.handlers.faq import register_handlers_faq
from maildelivery import sending_message, gen_secret_key
from config import BOT_TOKEN, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, webhook_url, cache
from states import BotStates
from services.registration import make_registration

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=RedisStorage2())

register_handlers_common(dp)
register_handlers_create_event(dp)
register_handlers_faq(dp)


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    await message.answer("Для регистрации в Ylab-боте введите команду /reg, "
                         "или /help для получения списка доступных команд.")
    await BotStates.STATE_0.set()


@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message):
    await BotStates.STATE_0.set()
    await message.answer("Здесь будет список доступных команд")


@dp.message_handler(commands=['reg'], state='*')
async def process_reg_command(message: types.Message):
    await message.answer("Здравствуйте, напишите адрес свой электронной почты "
                         "в домене @ylab.io для прохождения дальнейшей "
                         "регистрации!")
    await BotStates.STATE_1.set()


@dp.message_handler(state=BotStates.STATE_1)
async def email_message(message: types.Message):
    secret_key = gen_secret_key()
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data={'secret_key': secret_key})  # запись в Redis
    if '@ylab.io' in message.text:
        sending_message(message.text, secret_key)  # отправка письма на почту
        await message.answer("На вашу почту отправлен ключ "
                             "подтверждения введите его: ")
        await cache.update_data(chat=message.chat,
                                user=message.from_user.username,
                                data={
                                    'email': message.text})  # добавить email@ylab.io в Redis

        await BotStates.STATE_2.set()
    else:
        await message.answer("Вы ввели не корректный адрес")


@dp.message_handler(state=BotStates.STATE_2)
async def key_message(message: types.Message):
    secret_key = await cache.get_data(chat=message.chat,
                                      user=message.from_user.username)
    if secret_key['secret_key'] == message.text and await make_registration(message):
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
    else:
        await message.answer("Ошибка")


@dp.message_handler()
async def echo_message(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username,
                         data=message.text)  # запись в кэш
    await bot.send_message(message.from_user.id, message.text)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(webhook_url)


if __name__ == '__main__':
    # executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup,
                           skip_updates=True,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT)
