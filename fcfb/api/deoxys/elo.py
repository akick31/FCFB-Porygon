import requests
from fcfb.utils.exception_handling import async_exception_handler, DeoxysAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()
ELO_PATH = "elo/"


@async_exception_handler()
async def get_elo(team, week, season):
    """
    Make API call to get the ELO for a team in a given week of a given season
    :param team
    :param week
    :param season
    :return:
    """

    try:
        payload = f"team/{team}/week/{week}/season/{season}"
        endpoint = config_data['api']['url'] + ELO_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200:
            logger.info(f"Grabbed ELO for team {team} in week {week} of season {season}")
            return response.text
        else:
            logger.info(f"HTTP {response.status_code} response {response.text}")
            return "1500"
    except Exception as e:
        raise Exception(f"{e}")
