from .incorrect_passward_rate_limit import ThrottlingMiddleware
from .antiflood_middleware import AntiFloodThrottlingMiddleware
from loader import dp

from .incorrect_passward_rate_limit import ThrottlingMiddleware

dp.middleware.setup(ThrottlingMiddleware())
dp.middleware.setup(AntiFloodThrottlingMiddleware())
