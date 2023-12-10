import re


def extract_game_state_info(text):
    pattern = re.compile(r'Clock\|Quarter\|Down\|Ball Location\|Possession\|Playclock\|Deadline\n:-:\|:-:\|:-:\|:-:\|:-:\|:-:\|:-:\n(.+?)\n')
    match = pattern.search(text)
    if match:
        game_state_info = match.group(1).split('|')

        # Extracting team name and number from 'ball_location'
        ball_location_parts = re.match(r'(\d+) \[(.+)\]\(#f/(.+)\)', game_state_info[3].strip())
        if ball_location_parts:
            yard_line = ball_location_parts.group(1).strip()
            team_name = ball_location_parts.group(2).strip()
            game_state_info[3] = f"{team_name} {yard_line}"

        # Extracting team name from 'possession'
        team_name = game_state_info[4].split('[')[-1].split(']')[0]

        # Appending team name to the 'possession' value
        game_state_info[4] = f"{team_name}"

        return {
            'down_and_distance': game_state_info[2].strip(),
            'ball_location': game_state_info[3].strip(),
            'possession': game_state_info[4].strip()
        }
    return None


def extract_team_info(text):
    """
    Extract the team information from the text

    :param text:
    :return:
    """

    # Split the text into lines
    lines = text.split('\n')

    # Find the index of the line that starts the team information
    team_info_start_index = lines.index('Team|Coach(es)|Offense|Defense')

    # Extract team information
    team_lines = lines[team_info_start_index + 2:team_info_start_index + 4]
    teams = []
    for line in team_lines:
        if not line:  # Skip empty lines
            continue
        parts = line.split('|')
        team_name = parts[0].strip().split('[')[-1].split(']')[0]
        coach_name = parts[1].strip().replace('/u/', '')
        team = {
            'team': team_name,
            'coach': coach_name,
            'offense': parts[2].strip(),
            'defense': parts[3].strip(),
        }
        teams.append(team)

    if teams is None:
        return None

    team_info = {
        "home_team": teams[0]["team"],
        "away_team": teams[1]["team"],
        "home_coach": teams[0]["coach"],
        "away_coach": teams[1]["coach"],
        "home_offensive_playbook": teams[0]["offense"],
        "away_offensive_playbook": teams[1]["offense"],
        "home_defensive_playbook": teams[0]["defense"],
        "away_defensive_playbook": teams[1]["defense"],
    }

    return team_info


def extract_team_stats(text):
    """
    Extract the team stats from the text

    :param text:
    :return:
    """

    # Split the text into lines
    lines = text.split('\n')

    # Find the index of the first occurrence of the row header
    header_index = lines.index("Total Passing Yards|Total Rushing Yards|Total Yards|Interceptions Lost|Fumbles Lost|Field Goals|Time of Possession|Timeouts")

    # Find the index of the second occurrence of the row header
    second_header_index = lines[header_index + 1:].index("Total Passing Yards|Total Rushing Yards|Total Yards|Interceptions Lost|Fumbles Lost|Field Goals|Time of Possession|Timeouts") + header_index + 1

    # Extract team stats
    away_team_stats_line = lines[header_index + 2]
    home_team_stats_line = lines[second_header_index + 2]

    stats_parts_away_team = away_team_stats_line.split('|')
    stats_parts_home_team = home_team_stats_line.split('|')

    if away_team_stats_line is not None and home_team_stats_line is not None:
        return {
            'away_team_stats': {
                'total_passing_yards': stats_parts_away_team[0].strip(),
                'total_rushing_yards': stats_parts_away_team[1].strip(),
                'total_yards': stats_parts_away_team[2].strip(),
                'time_of_possession': stats_parts_away_team[6].strip(),
                'timeouts': stats_parts_away_team[7].strip()
            },
            'home_team_stats': {
                'total_passing_yards': stats_parts_home_team[0].strip(),
                'total_rushing_yards': stats_parts_home_team[1].strip(),
                'total_yards': stats_parts_home_team[2].strip(),
                'time_of_possession': stats_parts_home_team[6].strip(),
                'timeouts': stats_parts_home_team[7].strip()
            }
        }
    return None


def extract_waiting_on_and_gist(text):
    """
    Extract the waiting on and gist information from the text

    :param text:
    :return:
    """
    # Find the index of the relevant information
    plays_index = text.find("[Plays](")
    message_index = text.find("Waiting on a response from /u/")

    if plays_index != -1 and message_index != -1:
        # Extract waiting user
        waiting_user_start = message_index + len("Waiting on a response from /u/")
        waiting_user_end = text.find(" to this [message]", waiting_user_start)
        waiting_on_user = text[waiting_user_start:waiting_user_end].strip()
        # Extract only the username
        if " to this [comment]" in waiting_on_user:
            waiting_on_user = waiting_on_user.split(" to this [comment]")[0].strip()
        elif "Waiting on a response from" not in text:
            return None

        # Extract gist link
        gist_start = plays_index + len("[Plays](")
        gist_end = text.find(")", gist_start)
        gist_link = text[gist_start:gist_end].strip()

        if "https" not in gist_link:
            return None

        return {
            'waiting_on': waiting_on_user,
            'gist_link': gist_link
        }

    return None
