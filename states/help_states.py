from aiogram.dispatcher.filters.state import State, StatesGroup


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
