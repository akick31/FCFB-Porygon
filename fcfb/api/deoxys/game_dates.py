import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
GAME_DATES_PATH = "game_dates/"


@async_exception_handler()
async def get_game_season(thread_timestamp):
    """
    Make API call to get the season for a game
    :param thread_timestamp
    :return:
    """

    try:
        payload = f"season/{thread_timestamp}"
        endpoint = config_data['api']['url'] + GAME_DATES_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"Grabbed season for game with thread timestamp {thread_timestamp}")
            return response.text
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


@async_exception_handler()
async def get_game_week(thread_timestamp, season):
    """
    Make API call to get the week for a game
    :param thread_timestamp
    :param season
    :return:
    """

    try:
        payload = f"week/{thread_timestamp}/{season}"
        endpoint = config_data['api']['url'] + GAME_DATES_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"Grabbed week for game with thread timestamp {thread_timestamp} in season {season}")
            return response.text
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")