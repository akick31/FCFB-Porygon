import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
GAME_PLAYS_PATH = "games/"


@async_exception_handler()
async def save_game(game_id, game):
    """
    Make API call to save the game in the database
    :param game_id
    :param game
    :return:
    """

    try:
        payload = f"add"
        headers = {"Content-Type": "application/json"}
        endpoint = config_data['api']['url'] + GAME_PLAYS_PATH + payload
        response = requests.post(endpoint, data=game, headers=headers)

        if response.status_code == 201 or response.status_code == 200:
            logger.info(f"Submitted new game {game_id}")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


@async_exception_handler()
async def get_game(game_id):
    """
    Make API call to get the game from the database
    :param game_id
    :return:
    """

    try:
        payload = f"{game_id}"
        endpoint = config_data['api']['url'] + GAME_PLAYS_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"Game {game_id} retrieved")
            return response.json()
        elif response.status_code == 404:
            logger.info(f"Game {game_id} not found")
            return None
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


@async_exception_handler()
async def update_game(game_id, game):
    """
    Make API call to update the game in the database
    :param game_id
    :param game
    :return:
    """

    try:
        payload = f"update"
        headers = {"Content-Type": "application/json"}
        endpoint = config_data['api']['url'] + GAME_PLAYS_PATH + payload
        response = requests.put(endpoint, data=game, headers=headers)

        if response.status_code == 200:
            logger.info(f"Updated game {game_id}")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")