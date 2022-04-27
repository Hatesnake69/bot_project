from utils import get_logger

logger = get_logger(__name__)


def bq_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            await kwargs["message"].answer(
                text=("Произошла непредвиденная ошибка, "
                      "свяжитесь с администратором!")
            )
            await kwargs["state"].finish()
    return wrapper
