from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from keyboards import KEYBOARDS, FIN_STR, FWD_STR, BCK_STR, UP_STR, \
    ORG_STR, ACC_STR, TECH_STR, OTH_STR
from config import cache
from aiogram.dispatcher.filters.state import State, StatesGroup


async def update_state(message, new_state, keyboard, state):
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data=message.text)
    await state.set_state(new_state)
    await message.reply("choose",
                        reply_markup=KEYBOARDS[keyboard],
                        reply=False)


class HelpStates(StatesGroup):
    INIT_FIRST_STATE = State()
    INIT_SECOND_STATE = State()
    INIT_THIRD_STATE = State()
    FIN_FIRST_STATE = State()
    FIN_SECOND_STATE = State()
    FIN_THIRD_STATE = State()
    ORG_STATE = State()
    OTH_STATE = State()
    TECH_FIRST_STATE = State()
    TECH_SECOND_STATE = State()
    ACC_STATE = State()


async def process_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_to_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


async def fwd_to_second_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


async def fin_bck_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_fwd_third_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.FIN_THIRD_STATE,
                       "fin_third",
                       state)


async def fin_bck_first_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


async def fin_up_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_bck_second_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


async def fin_third_up_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_org_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.ORG_STATE,
                       "org",
                       state)


async def org_bck_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_acc_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.ACC_STATE,
                       "acc",
                       state)


async def acc_bck_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def tech_fwd_first_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


async def tech_fwd_second_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.TECH_SECOND_STATE,
                       "tech_second",
                       state)


async def tech_bck_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def tech_bck_first_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


async def tech_up_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_oth_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.OTH_STATE,
                       "oth",
                       state)


async def oth_bck_start_command(message: types.Message, state: FSMContext):
    await update_state(message,
                       HelpStates.INIT_FIRST_STATE,
                       "start",
                       state)


def register_handlers_faq(dp: Dispatcher):
    dp.register_message_handler(process_start_command,
                                state='*',
                                commands=['help'])
    dp.register_message_handler(fin_to_start_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[FIN_STR])
    dp.register_message_handler(fwd_to_second_command,
                                state=HelpStates.FIN_FIRST_STATE,
                                text=[FWD_STR])
    dp.register_message_handler(fin_bck_start_command,
                                state=HelpStates.FIN_FIRST_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(fin_fwd_third_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[FWD_STR])
    dp.register_message_handler(fin_bck_first_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(fin_up_start_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[UP_STR])
    dp.register_message_handler(fin_bck_second_command,
                                state=HelpStates.FIN_THIRD_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(fin_third_up_command,
                                state=HelpStates.FIN_THIRD_STATE,
                                text=[UP_STR])
    dp.register_message_handler(start_to_org_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[ORG_STR])
    dp.register_message_handler(org_bck_start_command,
                                state=HelpStates.ORG_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(start_to_acc_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[ACC_STR])
    dp.register_message_handler(acc_bck_start_command,
                                state=HelpStates.ACC_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(tech_fwd_first_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[TECH_STR])
    dp.register_message_handler(tech_fwd_second_command,
                                state=HelpStates.TECH_FIRST_STATE,
                                text=[FWD_STR])
    dp.register_message_handler(tech_bck_start_command,
                                state=HelpStates.TECH_FIRST_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(tech_bck_first_command,
                                state=HelpStates.TECH_SECOND_STATE,
                                text=[BCK_STR])
    dp.register_message_handler(tech_up_start_command,
                                state=HelpStates.TECH_SECOND_STATE,
                                text=[UP_STR])
    dp.register_message_handler(start_to_oth_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[OTH_STR])
    dp.register_message_handler(oth_bck_start_command,
                                state=HelpStates.OTH_STATE,
                                text=[BCK_STR]
                                )
