import pandas as pd
from aiogram.types import Message
from google.cloud import bigquery
from google.oauth2.service_account import Credentials

from data import CREDENTIALS_PATH, PROJECT


def bq_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            await kwargs["message"].reply("что-то не так!")

    return wrapper


class AsyncBQ:
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            CREDENTIALS_PATH
        )
        self.project = PROJECT
        self.bqclient = bigquery.Client(credentials=self.credentials)

    async def send_query(self, query: str) -> pd.DataFrame:
        return pd.read_gbq(
            query=query,
            project_id=self.project,
            credentials=self.credentials,
        )

    @bq_error_handler
    async def check_auth(self, message: Message) -> str:
        tg_id: int = message.from_user.id
        query: str = (
            f"SELECT telegram_id "
            f"FROM handy-digit-312214.TG_Bot_Stager.users "
            f"WHERE telegram_id = {tg_id} AND is_confirmed = false"
        )
        db_result = await self.send_query(query=query)
        return "Not auth" if db_result.empty else "Auth"

    @bq_error_handler
    async def check_user_role(self, message: Message) -> bool:
        tg_id: int = message.from_user.id
        query: str = (
            f"SELECT role "
            f"FROM handy-digit-312214.TG_Bot_Stager.users "
            f"WHERE telegram_id = {tg_id}"
        )
        db_result = await self.send_query(query=query)
        return db_result.values[0][0] == "admin"


async_db_manager = AsyncBQ()
