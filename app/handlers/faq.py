from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

import keyboards as key
from states import BotStates, update_state


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


async def process_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_to_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


async def fwd_to_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


async def fin_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_fwd_third_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.FIN_THIRD_STATE,
                       "fin_third",
                       state)


async def fin_bck_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


async def fin_up_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def fin_bck_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


async def fin_third_up_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_org_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.ORG_STATE,
                       "org",
                       state)


async def org_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_acc_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.ACC_STATE,
                       "acc",
                       state)


async def acc_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def tech_fwd_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


async def tech_fwd_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.TECH_SECOND_STATE,
                       "tech_second",
                       state)


async def tech_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def tech_bck_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


async def tech_up_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


async def start_to_oth_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.OTH_STATE,
                       "oth",
                       state)


async def oth_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       BotStates.INIT_FIRST_STATE,
                       "start",
                       state)


def register_handlers_faq(dp: Dispatcher):
    dp.register_message_handler(process_start_command,
                                state='*',
                                commands=['faq'])
    dp.register_message_handler(fin_to_start_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[key.FIN_STR])
    dp.register_message_handler(fwd_to_second_command,
                                state=HelpStates.FIN_FIRST_STATE,
                                text=[key.FWD_STR])
    dp.register_message_handler(fin_bck_start_command,
                                state=HelpStates.FIN_FIRST_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(fin_fwd_third_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[key.FWD_STR])
    dp.register_message_handler(fin_bck_first_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(fin_up_start_command,
                                state=HelpStates.FIN_SECOND_STATE,
                                text=[key.UP_STR])
    dp.register_message_handler(fin_bck_second_command,
                                state=HelpStates.FIN_THIRD_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(fin_third_up_command,
                                state=HelpStates.FIN_THIRD_STATE,
                                text=[key.UP_STR])
    dp.register_message_handler(start_to_org_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[key.ORG_STR])
    dp.register_message_handler(org_bck_start_command,
                                state=HelpStates.ORG_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(start_to_acc_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[key.ACC_STR])
    dp.register_message_handler(acc_bck_start_command,
                                state=HelpStates.ACC_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(tech_fwd_first_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[key.TECH_STR])
    dp.register_message_handler(tech_fwd_second_command,
                                state=HelpStates.TECH_FIRST_STATE,
                                text=[key.FWD_STR])
    dp.register_message_handler(tech_bck_start_command,
                                state=HelpStates.TECH_FIRST_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(tech_bck_first_command,
                                state=HelpStates.TECH_SECOND_STATE,
                                text=[key.BCK_STR])
    dp.register_message_handler(tech_up_start_command,
                                state=HelpStates.TECH_SECOND_STATE,
                                text=[key.UP_STR])
    dp.register_message_handler(start_to_oth_command,
                                state=HelpStates.INIT_FIRST_STATE,
                                text=[key.OTH_STR])
    dp.register_message_handler(oth_bck_start_command,
                                state=HelpStates.OTH_STATE,
                                text=[key.BCK_STR]
                                )
