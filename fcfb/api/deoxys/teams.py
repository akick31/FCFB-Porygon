import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
TEAMS_PATH = "teams/"


@async_exception_handler()
async def get_team(team_name):
    """
    Make API call to get the team from the database
    :param team_name
    :return:
    """

    try:
        payload = f"{team_name}"
        endpoint = config_data['api']['url'] + TEAMS_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"{team_name} retrieved")
            return response.json()
        elif response.status_code == 404:
            logger.info(f"{team_name} not found")
            return None
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")
