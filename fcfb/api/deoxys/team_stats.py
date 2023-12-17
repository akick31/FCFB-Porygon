import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
TEAMS_PATH = "team_stats/"


@async_exception_handler()
async def get_team_stats(team_name, season):
    """
    Make API call to get the team stats from the database
    :param team_name
    :param season
    :return:
    """

    try:
        payload = f"{team_name}/{season}"
        endpoint = config_data['api']['url'] + TEAMS_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"{team_name} stats retrieved")
            return response.json()
        elif response.status_code == 404:
            logger.info(f"{team_name} stats not found")
            return None
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


@async_exception_handler()
async def create_team_stats(team_name, season, team_stats):
    """
    Make API call to create the team stats in the database for the season

    :param team_name:
    :param season:
    :param team_stats:
    :return:
    """

    try:
        payload = f"create/{team_name}/{season}"
        headers = {"Content-Type": "application/json"}
        endpoint = config_data['api']['url'] + TEAMS_PATH + payload
        response = requests.put(endpoint, data=team_stats, headers=headers)

        if response.status_code == 200:
            logger.info(f"Created {team_name} stats")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


@async_exception_handler()
async def update_team_stats(team_name, season, team_stats):
    """
    Make API call to update the team stats in the database

    :param team_name:
    :param season:
    :param team_stats:
    :return:
    """

    try:
        payload = f"update/{team_name}/{season}"
        headers = {"Content-Type": "application/json"}
        endpoint = config_data['api']['url'] + TEAMS_PATH + payload
        response = requests.put(endpoint, data=team_stats, headers=headers)

        if response.status_code == 200:
            logger.info(f"Updated {team_name} stats")
            return response.status_code
        else:
            raise DeoxysAPIError(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")