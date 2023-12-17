import requests
from fcfb.utils.exception_handling import async_exception_handler, GistAPIError
from fcfb.utils.setup import setup

config_data, r, logger = setup()


@async_exception_handler()
async def extract_plays_from_gist(gist_url, home_team, away_team, game_id):
    """
    Extract the plays from the gist

    :param gist_url:
    :param home_team:
    :param away_team:
    :param game_id:
    :return:
    """

    try:
        # Get the Gist ID
        gist_id = gist_url.split("/")[-1]

        # Get the Gist content
        headers = {"Authorization": f"Bearer {config_data['github']['token']}"}
        response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
        gist_data = response.json()

        file_name = list(gist_data["files"].keys())[-1]
        file_content = gist_data["files"][file_name]["content"]

        # Get a dictionary of plays
        plays = get_plays(file_content, home_team, away_team, game_id)

        return plays
    except Exception as e:
        raise GistAPIError(f"{e}")


def get_plays(gist_content, home_team, away_team, game_id):
    """
    Get the plays from the gist

    :return:
    """

    # Split the content into lines
    lines = gist_content.strip().split('\n')

    # Find the index of the header line
    header_index = lines.index("Home score|Away score|Quarter|Clock|Ball Location|Possession|Down|Yards to go|Defensive number|Offensive number|Defensive submitter|Offensive submitter|Play|Result|Actual result|Yards|Play time|Runoff time")

    # Extract headers and remove any leading/trailing spaces
    headers = [header.strip() for header in lines[header_index].split('|')]

    # Initialize an empty list to store dictionaries
    parsed_data = []

    # Iterate through lines, starting from the line after the header
    play_number = 0
    for line in lines[header_index + 1:]:
        # Skip lines with "-----"
        if line.startswith("-"):
            continue

        # Increment the play number
        play_number += 1

        # Split the line by "|" and create a dictionary
        values = [value.strip() for value in line.split('|')]
        row_dict = dict(zip(headers, values))

        # Add additional information to the dictionary
        row_dict['home_team'] = home_team
        row_dict['away_team'] = away_team
        row_dict['game_id'] = game_id
        row_dict['play_number'] = play_number

        # Calculate the win probability
        win_probability = 0.0
        row_dict['win_probability'] = win_probability

        # Append the dictionary to the list
        parsed_data.append(row_dict)

    return parsed_data
