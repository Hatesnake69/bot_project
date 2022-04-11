from .incorrect_passward_rate_limit import ThrottlingMiddleware
from loader import dp

dp.middleware.setup(ThrottlingMiddleware())
