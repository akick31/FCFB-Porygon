import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
GAME_PLAYS_PATH = "games/"


@async_exception_handler()
async def save_game(game):
    """
    Make API call to save the play in the database
    :param game
    :return:
    """

    try:
        payload = f"add"
        headers = {"Content-Type": "application/json"}
        endpoint = config_data['api']['url'] + GAME_PLAYS_PATH + payload
        response = requests.post(endpoint, data=game, headers=headers)

        if response.status_code == 201:
            logger.info(f"Submitted new game {game['game_id']} between {game['home_team']} and {game['away_team']}")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")