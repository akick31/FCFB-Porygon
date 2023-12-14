from fcfb.api.deoxys.elo import get_elo

# Vegas line divisor - (Elo - Opp Elo / x)
vegas_divisor = 18.14010981807


async def calculate_spread(team_info, season, week):
    """
    Calculate the spread for a given game

    :param team_info:
    :param season:
    :param week:
    :return:
    """

    home_team = team_info['home_team']
    away_team = team_info['away_team']
    week = int(week)

    home_elo = float(await get_elo(home_team, week-1, season))
    away_elo = float(await get_elo(away_team, week-1, season))

    return {"spread": (home_elo - away_elo) / vegas_divisor}
