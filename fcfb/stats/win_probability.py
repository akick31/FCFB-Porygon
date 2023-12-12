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