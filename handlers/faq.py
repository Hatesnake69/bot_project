from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import keyboards as key
from loader import dp
from states import FaqStates, update_state


@dp.message_handler(commands=['faq'], state='*')
async def process_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.FIN_STR], state=FaqStates.INIT_FIRST_STATE)
async def fin_to_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


@dp.message_handler(text=[key.FWD_STR], state=FaqStates.FIN_FIRST_STATE)
async def fwd_to_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.FIN_FIRST_STATE)
async def fin_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.FWD_STR], state=FaqStates.FIN_SECOND_STATE)
async def fin_fwd_third_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.FIN_THIRD_STATE,
                       "fin_third",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.FIN_SECOND_STATE)
async def fin_bck_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.FIN_FIRST_STATE,
                       "fin_first",
                       state)


@dp.message_handler(text=[key.UP_STR], state=FaqStates.FIN_SECOND_STATE)
async def fin_up_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.FIN_THIRD_STATE)
async def fin_bck_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.FIN_SECOND_STATE,
                       "fin_second",
                       state)


@dp.message_handler(text=[key.UP_STR], state=FaqStates.FIN_THIRD_STATE)
async def fin_third_up_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.ORG_STR], state=FaqStates.INIT_FIRST_STATE)
async def start_to_org_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.ORG_STATE,
                       "org",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.ORG_STATE)
async def org_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.ACC_STR], state=FaqStates.INIT_FIRST_STATE)
async def start_to_acc_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.ACC_STATE,
                       "acc",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.ACC_STATE)
async def acc_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.TECH_STR], state=FaqStates.INIT_FIRST_STATE)
async def tech_fwd_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


@dp.message_handler(text=[key.FWD_STR], state=FaqStates.TECH_FIRST_STATE)
async def tech_fwd_second_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.TECH_SECOND_STATE,
                       "tech_second",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.TECH_FIRST_STATE)
async def tech_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.TECH_SECOND_STATE)
async def tech_bck_first_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.TECH_FIRST_STATE,
                       "tech_first",
                       state)


@dp.message_handler(text=[key.UP_STR], state=FaqStates.TECH_SECOND_STATE)
async def tech_up_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)


@dp.message_handler(text=[key.OTH_STR], state=FaqStates.INIT_FIRST_STATE)
async def start_to_oth_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.OTH_STATE,
                       "oth",
                       state)


@dp.message_handler(text=[key.BCK_STR], state=FaqStates.OTH_STATE)
async def oth_bck_start_command(message: Message, state: FSMContext):
    await update_state(message,
                       FaqStates.INIT_FIRST_STATE,
                       "start",
                       state)
