import math
import xgboost as xgb
import os
import pandas as pd

from fcfb.api.deoxys.elo import get_elo

absolute_path = os.path.dirname(os.path.abspath(__file__))

model_xgb = xgb.XGBRegressor()
model_xgb.load_model(absolute_path + '/model/wpmodel.json')

data = {
    'down': [4],
    'distance': [4],
    'position': [38],
    'margin': [17],
    'seconds_left_game': [350],
    'seconds_left_half': [350],
    'half': [2],
    'had_first_possession': [1],
    'elo_diff_time': [27.0449]
}


async def calculate_win_probability(team_info, plays, game_date_info):
    """
    Calculate the win probability for each play in a game

    :param team_info:
    :param plays:
    :param game_date_info:
    :return:
    """

    try:
        week = game_date_info['week']
        season = game_date_info['season']
        home_team = team_info['home_team']
        away_team = team_info['away_team']

        home_elo = await get_elo(home_team, week, season)
        away_elo = await get_elo(away_team, week, season)

        had_first_possession = 0 if plays[1]['Possession'] == "home" else 1

        for play in plays:
            play_type = play['Play']
            quarter = int(play['Quarter'])
            clock = int(play['Clock'])
            play_number = int(play['play_number'])
            if play['Possession'] == home_team:
                margin = int(play['Home score']) - int(play['Away score'])
                offense_elo = home_elo
                defense_elo = away_elo
            else:
                margin = int(play['Away score']) - int(play['Home score'])
                offense_elo = away_elo
                defense_elo = home_elo

            position = 100 - int(play['Ball Location'])
            down = int(play['Down'])
            distance = int(play['Yards to go'])

            # Calculate the time remaining in the game
            if quarter == 1:
                seconds_left_game = 1680 - (420 - clock)
                seconds_left_half = 840 - (420 - clock)
                half = 1
            elif quarter == 2:
                seconds_left_game = 1260 - (420 - clock)
                seconds_left_half = clock
                half = 1
            elif quarter == 3:
                seconds_left_game = 840 - (420 - clock)
                seconds_left_half = 840 - (420 - clock)
                half = 2
            else:
                seconds_left_game = clock
                seconds_left_half = clock
                half = 2

            # Calculate the difference in Elo between the offense and defense
            elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

            current_win_probability = get_win_probability_for_play(down, distance, position, margin, seconds_left_game,
                                                                   seconds_left_half, half, had_first_possession,
                                                                   elo_diff_time, play_type)
            plays[play_number]['win_probability'] = current_win_probability

        return plays
    except Exception as e:
        raise Exception(f"{e}")


def get_win_probability_for_play(down, distance, position, margin, seconds_left_game, seconds_left_half, half,
                                 had_first_possession, elo_diff_time, play_type):
    """
    Get the win probability for the play, recursively

    :param down:
    :param distance:
    :param position:
    :param margin:
    :param seconds_left_game:
    :param seconds_left_half:
    :param half:
    :param had_first_possession:
    :param elo_diff_time:
    :param play_type:
    :return:
    """

    try:
        if seconds_left_game == 0 and play_type != "PAT":
            return 1 if margin > 0 else (0 if margin < 0 else 0.5)

        if play_type == "PAT":
            prob_if_success = get_win_probability_for_play(1, 10, 75, -(margin + 1), seconds_left_game,
                                                           seconds_left_half, half, 1 - had_first_possession,
                                                           -elo_diff_time, 'RUN')
            prob_if_fail = get_win_probability_for_play(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                                        1 - had_first_possession, -elo_diff_time, 'RUN')
            prob_if_return = get_win_probability_for_play(1, 10, 75, -(margin - 2), seconds_left_game,
                                                          seconds_left_half, half, 1 - had_first_possession,
                                                          -elo_diff_time, 'RUN')
            return 1 - (((721 / 751) * prob_if_success) + ((27 / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
        if play_type == 'TWO_POINT':
            prob_if_success = get_win_probability_for_play(1, 10, 75, -(margin + 2), seconds_left_game,
                                                           seconds_left_half, half, 1 - had_first_possession,
                                                           -elo_diff_time, 'RUN')
            prob_if_fail = get_win_probability_for_play(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                                        1 - had_first_possession, -elo_diff_time, 'RUN')
            prob_if_return = get_win_probability_for_play(1, 10, 75, -(margin - 2), seconds_left_game,
                                                          seconds_left_half, half, 1 - had_first_possession,
                                                          -elo_diff_time, 'RUN')
            return 1 - (((301 / 751) * prob_if_success) + ((447 / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
        if play_type == 'KICKOFF_NORMAL':
            return 1 - get_win_probability_for_play(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                                    1 - had_first_possession, -elo_diff_time, 'RUN')
        if play_type == 'KICKOFF_SQUIB':
            slh = max(seconds_left_half - 5, 0)
            slg = ((2 - half) * 840) + slh
            return 1 - get_win_probability_for_play(1, 10, 65, -margin, slg, slh, half, 1 - had_first_possession,
                                                    -elo_diff_time, 'RUN')
        if play_type == 'KICKOFF_ONSIDE':
            slh = max(seconds_left_half - 3, 0)
            slg = ((2 - half) * 840) + slh
            prob_if_success = get_win_probability_for_play(1, 10, 55, margin, slg, slh, half, 1 - had_first_possession,
                                                           elo_diff_time, 'RUN')
            prob_if_fail = 1 - get_win_probability_for_play(1, 10, 45, -margin, slg, slh, half,
                                                            1 - had_first_possession, -elo_diff_time, 'RUN')
            slhr = max(seconds_left_half - 10, 0)
            slgr = ((2 - half) * 840) + slh
            prob_if_return = 1 - get_win_probability_for_play(1, 10, 75, margin - 6, slgr, slhr, half,
                                                              1 - had_first_possession,
                                                              -elo_diff_time, 'PAT')
            return ((140 / 751) * prob_if_success) + ((611 / 751) * prob_if_fail) + ((1 / 751) * prob_if_return)

        data["had_first_possession"] = [had_first_possession]
        data["margin"] = [margin]
        data["down"] = [down]
        data["distance"] = [distance]
        data["position"] = [position]
        data["seconds_left_game"] = [seconds_left_game]
        data["seconds_left_half"] = [seconds_left_half]
        data["half"] = [half]
        data["elo_diff_time"] = [elo_diff_time]

        df_data = pd.DataFrame.from_dict(data)
        win_probability = model_xgb.predict(df_data)
        return float(win_probability)
    except Exception as e:
        raise Exception(f"{e}")
