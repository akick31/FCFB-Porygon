import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
GAME_PLAYS_PATH = "game_plays/"


@async_exception_handler()
async def save_play(play_data):
    """
    Make API call to save the play in the database
    :param play_data
    :return:
    """

    try:
        formatted_data = {key.lower().replace(' ', '_'): value for key, value in play_data.items()}
        payload = f"add/{'/'.join(f'{key}/{value}' for key, value in formatted_data.items())}"
        endpoint = config_data['api']['url'] + GAME_PLAYS_PATH + payload
        response = requests.post(endpoint)

        if response.status_code == 201:
            logger.info(f"Submitted play for game {play_data['game_id']}")
            return response.status_code
        elif response.status_code == 200:
            logger.info(f"Play was already submitted for game {play_data['game_id']}, ignoring")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")