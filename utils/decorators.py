import logging

logging.basicConfig(
    filename="logging/bot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s- %(levelname)s : %(message)s",
)


def bq_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            await kwargs["message"].answer("Произошла непредвиденная ошибка, "
                                           "свяжитесь с администратором!")
            await kwargs["state"].finish()
    return wrapper
