import functools

from fcfb.utils.setup import setup

config_data, r, logger = setup()


class DiscordAPIError(Exception):
    pass


class RedditAPIError(Exception):
    pass


class GameError(Exception):
    pass


class GistAPIError(Exception):
    pass


class InvalidParameterError(ValueError):
    pass


class DeoxysAPIError(Exception):
    pass


def async_exception_handler():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except DiscordAPIError as dae:
                error_message = f"Discord API error in {func.__name__}(): {dae}"
                logger.error(error_message)
                raise dae
            except RedditAPIError as re:
                error_message = f"Reddit API error in {func.__name__}(): {re}"
                logger.error(error_message)
                raise re
            except GistAPIError as ge:
                error_message = f"Gist API error in {func.__name__}(): {ge}"
                logger.error(error_message)
                raise ge
            except InvalidParameterError as ipe:
                error_message = f"Invalid parameter error in {func.__name__}(): {ipe}"
                logger.error(error_message)
                raise ipe
            except GameError as ge:
                error_message = f"Game error in {func.__name__}(): {ge}"
                logger.error(error_message)
                raise ge
            except DeoxysAPIError as de:
                error_message = f"Deoxys API error in {func.__name__}(): {de}"
                logger.error(error_message)
                raise de
            except Exception as e:
                error_message = f"An unexpected error occurred in {func.__name__}(): {e}"
                logger.error(error_message)
                raise e
        return wrapper
    return decorator
