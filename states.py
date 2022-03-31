from aiogram import types
from utils import HelpStates
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import *
from bot import bot
from config import cache
from aiogram.dispatcher.filters.state import State, StatesGroup

dp = Dispatcher(bot, storage=MemoryStorage())


async def update_state(message, cond, keyboard):
    state = dp.current_state(user=message.from_user.id)
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)
    await state.set_state(cond)
    await message.reply('choose', reply_markup=KEYBOARDS[keyboard], reply=False)


@dp.message_handler(state='*', commands=['help'])
async def process_start_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.INIT_FIRST_STATE, text=[FIN_STR])
async def process_fin_command(message: types.Message):
    await update_state(message, HelpStates.FIN_FIRST_STATE, 'fin_first')


@dp.message_handler(state=HelpStates.FIN_FIRST_STATE, text=[FWD_STR])
async def process_fwd_command(message: types.Message):
    await update_state(message, HelpStates.FIN_SECOND_STATE, 'fin_second')


@dp.message_handler(state=HelpStates.FIN_FIRST_STATE, text=[BCK_STR])
async def process_bck_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.FIN_SECOND_STATE, text=[FWD_STR])
async def process_fwd_command(message: types.Message):
    await update_state(message, HelpStates.FIN_THIRD_STATE, 'fin_third')


@dp.message_handler(state=HelpStates.FIN_SECOND_STATE, text=[BCK_STR])
async def process_bck_command(message: types.Message):
    await update_state(message, HelpStates.FIN_FIRST_STATE, 'fin_first')


@dp.message_handler(state=HelpStates.FIN_SECOND_STATE, text=[UP_STR])
async def process_up_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.FIN_THIRD_STATE, text=[BCK_STR])
async def process_bck_command(message: types.Message):
    await update_state(message, HelpStates.FIN_SECOND_STATE, 'fin_second')


@dp.message_handler(state=HelpStates.FIN_THIRD_STATE, text=[UP_STR])
async def process_up_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.INIT_FIRST_STATE, text=[ORG_STR])
async def process_org_command(message: types.Message):
    await update_state(message, HelpStates.ORG_STATE, 'org')


@dp.message_handler(state=HelpStates.ORG_STATE, text=[BCK_STR])
async def process_org_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.INIT_FIRST_STATE, text=[ACC_STR])
async def process_acc_command(message: types.Message):
    await update_state(message, HelpStates.ACC_STATE, 'acc')


@dp.message_handler(state=HelpStates.ACC_STATE, text=[BCK_STR])
async def process_org_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.INIT_FIRST_STATE, text=[TECH_STR])
async def process_tech_command(message: types.Message):
    await update_state(message, HelpStates.TECH_FIRST_STATE, 'tech_first')


@dp.message_handler(state=HelpStates.TECH_FIRST_STATE, text=[FWD_STR])
async def process_fwd_command(message: types.Message):
    await update_state(message, HelpStates.TECH_SECOND_STATE, 'tech_second')


@dp.message_handler(state=HelpStates.TECH_FIRST_STATE, text=[BCK_STR])
async def process_bck_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.TECH_SECOND_STATE, text=[BCK_STR])
async def process_bck_command(message: types.Message):
    await update_state(message, HelpStates.TECH_FIRST_STATE, 'tech_first')


@dp.message_handler(state=HelpStates.TECH_SECOND_STATE, text=[UP_STR])
async def process_up_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state=HelpStates.INIT_FIRST_STATE, text=[OTH_STR])
async def process_oth_command(message: types.Message):
    await update_state(message, HelpStates.OTH_STATE, 'oth')


@dp.message_handler(state=HelpStates.OTH_STATE, text=[BCK_STR])
async def process_org_command(message: types.Message):
    await update_state(message, HelpStates.INIT_FIRST_STATE, 'start')


@dp.message_handler(state='*')
async def echo_message(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    current_state = await state.get_state()
    print('echo', msg, current_state)
    await bot.send_message(msg.from_user.id, msg.text)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


class BotStates(StatesGroup):
    """
    Класс описывает состояния функций

    Состояния:
    STATE_0 -- Нулевое состояние для запуска различных команд /start, /help ...
    в этом состоянии большинство handlers неактивны
    STATE_1 -- активирует def email_message()
    STATE_2 -- активирует def key_message()
    """
    STATE_0 = State()
    STATE_1 = State()
    STATE_2 = State()
