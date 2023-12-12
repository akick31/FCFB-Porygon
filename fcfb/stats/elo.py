import math
from fcfb.api.deoxys.elo import get_elo

# Vegas line divisor - (Elo - Opp Elo / x)
vegas_divisor = 18.14010981807

# MOV Standard Deviation - MOVs' standard deviation from the vegas line
mov_stdev = 15.61

# K value
k_val = 20


# P-F-R method - see https://www.pro-football-reference.com/about/win_prob.htm
def calc_win_prob(team_score, opp_score, team_elo, opp_elo, mins_played):
    """
    Calculate the win probability for a given game state

    :param team_score:
    :param opp_score:
    :param team_elo:
    :param opp_elo:
    :param mins_played:
    :return:
    """

    opp_margin = opp_score - team_score
    inverse_vegas_line = (team_elo - opp_elo) / vegas_divisor
    mins_remaining = (28 - mins_played)

    win_dist = cdf_normal((opp_margin + 0.5), (inverse_vegas_line * (mins_remaining / 28)), (mov_stdev / math.sqrt(28 / mins_remaining)))
    loss_dist = cdf_normal((opp_margin - 0.5), (inverse_vegas_line * (mins_remaining / 28)), (mov_stdev / math.sqrt(28 / mins_remaining)))

    win_prob = (1 - win_dist) + (0.5 * (win_dist - loss_dist))

    return win_prob


def cdf_normal(x, mean, stdev):
    """
    Cumulative distribution function for the normal distribution

    :param x:
    :param mean:
    :param stdev:
    :return:
    """

    return (1 - math.erf((mean - x) / (math.sqrt(2) * stdev))) / 2


def calc_mov_multiplier(score_diff, winner_elo_diff):
    """
    Calculate the MOV multiplier

    :param score_diff:
    :param winner_elo_diff:
    :return:
    """

    return math.log(abs(score_diff) + 1) * (2.2 / ((winner_elo_diff * 0.001) + 2.2))


# Don't calculate this every time
exp_normalizer = (1 - math.exp(0 - (28 / 2))) * 2


def calc_elo_change(mins_played, team_win_prob, mov_multiplier, expected_team_win_prob):
    """
    Calculate the Elo change for a given game

    :param mins_played:
    :param team_win_prob:
    :param mov_multiplier:
    :param expected_team_win_prob:
    :return:
    """

    # Deweight Elo changes for games with very short lengths
    exp_deweight = (((1 - math.exp(0 - (mins_played / 2))) * 2) / exp_normalizer)

    # Difference between result and expected result
    diff_from_expected = team_win_prob - expected_team_win_prob

    return exp_deweight * mov_multiplier * k_val * diff_from_expected


def calc_game_elo(game_json):
    """
    Calculate the Elo for a given game

    :param game_json:
    :return:
    """

    # Cap at 28 for overtime games
    #TODO get game length
    mins = min(game.get_game_length() / 60, 28)

    home_team = game_json['home_team']
    away_team = game_json['away_team']

    game_week = game_json['week']
    game_season = game_json['season']

    home_score = game_json['home_score']
    away_score = game_json['away_score']

    home_elo = await get_elo(home_team, game_week.week_no - 1, game_season)
    away_elo = await get_elo(away_team, game_week.week_no - 1, game_season)

    winner_elo_diff = 0

    if home_score > away_score:
        winner_elo_diff = home_elo - away_elo
    elif away_score > home_score:
        winner_elo_diff = away_elo - home_elo

    home_win_prob = calc_win_prob(home_score, away_score, home_elo, away_elo, mins)
    mov_multiplier = calc_mov_multiplier(home_score - away_score, winner_elo_diff)

    # 0 score diff and 0 minutes played = pre-game odds
    expected_home_win_prob = calc_win_prob(0, 0, home_elo, away_elo, 0)

    home_elo_change = calc_elo_change(mins, home_win_prob, mov_multiplier, expected_home_win_prob)
    away_elo_change = 0 - home_elo_change

    new_home_elo = home_elo + home_elo_change
    new_away_elo = away_elo + away_elo_change

    #TODO save elo

    return {
        'game': game,
        'home_team': home_team,
        'away_team': away_team,
        'home_elo': {
            'opp_elo': away_elo,
            'old_elo': home_elo,
            'elo': new_home_elo,
        },
        'away_elo': {
            'opp_elo': home_elo,
            'old_elo': away_elo,
            'elo': new_away_elo,
        },
    }
