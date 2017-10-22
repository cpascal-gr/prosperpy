import functools
import logging
import traceback

import autotrade

LOGGER = logging.getLogger(__name__)


def fatal(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            LOGGER.fatal("Error '%s' occurred when running '%s(%s, %s)'", ex, func, args, kwargs)
            LOGGER.fatal(traceback.format_exc())
            LOGGER.info('Stopping %s', autotrade.engine)
            autotrade.engine.stop()
    return wrapper
