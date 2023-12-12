import math
from models.team_metrics import TeamMetrics  # Assuming you have the necessary imports for models

# Vegas line divisor - (Elo - Opp Elo / x)
vegas_divisor = 18.14010981807

# MOV Standard Deviation - MOVs' standard deviation from the vegas line
mov_stdev = 15.61

# K value
k_val = 20

def get_elo(team, week_no, season):
    """
    Get the Elo for a team in a given week

    :param team:
    :param week_no:
    :param season:
    :return:
    """

    if not season:
        return 1500

    team_metrics = TeamMetrics.objects.get(team=team.id)
    found_season = False

    for metrics_season in team_metrics.seasons:
        if metrics_season.season == season.id:
            found_season = True

            for metrics_week in reversed(metrics_season.weeks):
                if 'week' not in metrics_week:
                    return metrics_week['elo']['elo']

                if week_no is not None:
                    metrics_week_doc = Week.objects.get(id=metrics_week['week'])

                    if metrics_week_doc.week_no <= week_no:
                        return metrics_week['elo']['elo']

    if not found_season:
        return 1500

    raise ValueError(f"Could not find S{season.season_no if season else '--'} W{week_no or '--'} metrics for {team.name}")

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


def calc_game_elo(game_id):
    """
    Calculate the Elo for a given game

    :param game_id:
    :return:
    """

    game = Game.objects.get(id=game_id)

    if not game or game.live:
        return False

    # Cap at 28 for overtime games
    mins = min(game.get_game_length() / 60, 28)

    home_team = Team.objects.get(id=game.home_team.team)
    away_team = Team.objects.get(id=game.away_team.team)

    game_week = Week.objects.get(games=game.id)
    game_season = Season.objects.get(id=game_week.season)

    home_score = game.home_team.stats.score.final
    away_score = game.away_team.stats.score.final

    home_elo = get_elo(home_team, game_week.week_no - 1, game_season)
    away_elo = get_elo(away_team, game_week.week_no - 1, game_season)

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