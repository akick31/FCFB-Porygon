import sys

sys.path.append("..")

from fcfb.utils.sheets_functions import *

"""
Handle calculating vegas odds for games

@author: apkick
"""

def get_elo(team, team_elo_column, elo_data_column):
    """
    Get the team Elo for the team requested

    :param team:
    :param team_elo_column:
    :param elo_data_column:
    :return:
    """

    team_column = team_elo_column
    elo_column = elo_data_column
    elo = 0
    i = 0
    for value in team_column:
        if "(" in value:
            value = value.split("(")[0]
            value = value.strip()
        if team == value:
            elo = elo_column[i]
            break
        i = i + 1
    if elo == 0:
        return -500
    return elo


def calculate_vegas_odds(team_elo, opponent_elo):
    """
    Calculate Vegas odds using a constant and team and their opponent Elo

    :param team_elo:
    :param opponent_elo:
    :return:
    """

    constant = 18.14010981807
    odds = (float(opponent_elo) - float(team_elo))/constant
    return odds

def get_vegas_odds(home_team, away_team):
    """
    Return a dictionary containing the Vegas Odds for the game

    :param home_team:
    :param away_team:
    :return:
    """

    elo_dictionary = get_elo_data()
    if elo_dictionary != "There was an error in contacting Google Sheets, please try again.":
        team_elo_column = elo_dictionary[1]
        elo_data_column = elo_dictionary[2]
        home_elo = get_elo(home_team, team_elo_column, elo_data_column)
        away_elo = get_elo(away_team, team_elo_column, elo_data_column)
        home_odds = calculate_vegas_odds(home_elo, away_elo)
        away_odds = calculate_vegas_odds(away_elo, home_elo)
        # Default to a push if can't find Elo
        if home_elo == -500 or away_elo == -500:
            home_odds = 0
            away_odds = 0
        return{0: home_odds, 1: away_odds}
    else:
        return elo_dictionary
    
    

