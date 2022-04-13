from loader import dp

from .incorrect_passward_rate_limit import ThrottlingMiddleware

dp.middleware.setup(ThrottlingMiddleware())
