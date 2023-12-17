from fcfb.api.deoxys.teams import get_team


async def calculate_team_stats(game_json):
    """
    Calculate the team stats for a game

    :param game_json:
    :return:
    """

    home_team_info = await get_team(game_json['home_team'])
    away_team_info = await get_team(game_json['away_team'])

    is_conference_game = False
    if home_team_info['conference'] is not None and away_team_info['conference'] is not None:
        if home_team_info['conference'] == away_team_info['conference']:
            is_conference_game = True

    num_plays = home_team_info['num_plays'] + game_json['num_plays']
    total_yards = home_team_info['total_yards'] + game_json['home_total_yards']
    passing_yards = home_team_info['passing_yards'] + game_json['home_passing_yards']
    rushing_yards = home_team_info['rushing_yards'] + game_json['home_rushing_yards']
    # Convert TOP to seconds, add, then convert back to string
    minutes = game_json['home_time_of_possession'].split(":")[0]
    seconds = game_json['home_time_of_possession'].split(":")[1]
    game_top = int(minutes) * 60 + int(seconds)
    minutes = home_team_info['time_of_possession'].split(":")[0]
    seconds = home_team_info['time_of_possession'].split(":")[1]
    current_total_top = int(minutes) * 60 + int(seconds)
    total_top = current_total_top + game_top
    minutes = str(int(total_top / 60))
    seconds = str(total_top % 60)
    time_of_possession = minutes + ":" + seconds
    field_goal_attempts = home_team_info['field_goal_attempts'] + game_json['home_field_goal_attempts']
    field_goal_makes = home_team_info['field_goal_makes'] + game_json['home_field_goal_successes']
    field_goal_percentage = field_goal_makes / field_goal_attempts

    if game_json['home_longest_field_goal'] > home_team_info['longest_field_goal']:
        longest_field_goal = game_json['home_longest_field_goal']
    else:
        longest_field_goal = home_team_info['longest_field_goal']

    if game_json['home_longest_touchdown'] > home_team_info['longest_touchdown']:
        longest_touchdown = game_json['home_longest_touchdown']
    else:
        longest_touchdown = home_team_info['longest_touchdown']

    passing_attempts = home_team_info['passing_attempts'] + game_json['home_passing_attempts']
    passing_completions = home_team_info['passing_completions'] + game_json['home_passing_completions']
    passing_percentage = passing_completions / passing_attempts
    passing_touchdowns = home_team_info['passing_touchdowns'] + game_json['home_passing_touchdowns']
    rushing_attempts = home_team_info['rushing_attempts'] + game_json['home_rushing_attempts']
    rushing_successes = home_team_info['rushing_successes'] + game_json['home_rushing_successes']
    rushing_percentage = rushing_successes / rushing_attempts
    rushing_touchdowns = home_team_info['rushing_touchdowns'] + game_json['home_rushing_touchdowns']
    third_down_attempts = home_team_info['third_down_attempts'] + game_json['home_third_down_attempts']
    third_down_successes = home_team_info['third_down_successes'] + game_json['home_third_down_successes']
    third_down_percentage = third_down_successes / third_down_attempts
    fourth_down_attempts = home_team_info['fourth_down_attempts'] + game_json['home_fourth_down_attempts']
    fourth_down_successes = home_team_info['fourth_down_successes'] + game_json['home_fourth_down_successes']
    fourth_down_percentage = fourth_down_successes / fourth_down_attempts
    two_point_attempts = home_team_info['two_point_attempts'] + game_json['home_two_point_attempts']
    two_point_successes = home_team_info['two_point_successes'] + game_json['home_two_point_successes']
    two_point_percentage = two_point_successes / two_point_attempts
    onside_kick_attempts = home_team_info['onside_kick_attempts'] + game_json['home_onside_kick_attempts']
    onside_kick_successes = home_team_info['onside_kick_successes'] + game_json['home_onside_kick_successes']
    onside_kick_percentage = onside_kick_successes / onside_kick_attempts
    offensive_plays = home_team_info['offensive_plays'] + game_json['home_offensive_plays']
    defensive_plays = home_team_info['defensive_plays'] + game_json['home_defensive_plays']
    turnovers = home_team_info['turnovers'] + game_json['home_turnovers']
    fumbles = home_team_info['fumbles'] + game_json['home_fumbles']
    interceptions = home_team_info['interceptions'] + game_json['home_interceptions']
    defensive_touchdowns = home_team_info['defensive_touchdowns'] + game_json['home_defensive_touchdowns']
    scoop_and_scores = home_team_info['scoop_and_scores'] + game_json['home_scoop_and_scores']
    pick_sixes = home_team_info['pick_sixes'] + game_json['home_pick_sixes']
    kickoff_defensive_touchdowns = home_team_info['kickoff_defensive_touchdowns'] + \
                                   game_json['home_kickoff_defensive_touchdowns']
    safeties_forced = home_team_info['safeties_forced'] + game_json['home_safeties_forced']
    safeties_allowed = home_team_info['safeties_allowed'] + game_json['away_safeties_forced']
    passing_yards_against = home_team_info['passing_yards_against'] + game_json['away_passing_yards']
    rushing_yards_against = home_team_info['rushing_yards_against'] + game_json['away_rushing_yards']
    # Convert TOP to seconds, add, then convert back to string
    minutes = game_json['away_time_of_possession'].split(":")[0]
    seconds = game_json['away_time_of_possession'].split(":")[1]
    game_top = int(minutes) * 60 + int(seconds)
    minutes = home_team_info['time_of_possession_against'].split(":")[0]
    seconds = home_team_info['time_of_possession_against'].split(":")[1]
    current_total_top = int(minutes) * 60 + int(seconds)
    total_top = current_total_top + game_top
    minutes = str(int(total_top / 60))
    seconds = str(total_top % 60)
    time_of_possession_against = minutes + ":" + seconds
    field_goal_attempts_against = home_team_info['field_goal_attempts_against'] + game_json['away_field_goal_attempts']
    field_goal_makes_against = home_team_info['field_goal_makes_against'] + game_json['away_field_goal_successes']
    field_goal_percentage_against = field_goal_makes_against / field_goal_attempts_against

    if game_json['away_longest_field_goal'] > home_team_info['longest_field_goal_against']:
        longest_field_goal_against = game_json['away_longest_field_goal']
    else:
        longest_field_goal_against = home_team_info['longest_field_goal_against']
    if game_json['away_longest_touchdown'] > home_team_info['longest_touchdown_against']:
        longest_touchdown_against = game_json['away_longest_touchdown']
    else:
        longest_touchdown_against = home_team_info['longest_touchdown_against']
    passing_attempts_against = home_team_info['passing_attempts_against'] + game_json['away_passing_attempts']
    passing_completions_against = home_team_info['passing_completions_against'] + game_json['away_passing_completions']
    passing_percentage_against = passing_completions_against / passing_attempts_against
    passing_touchdowns_against = home_team_info['passing_touchdowns_against'] + game_json['away_passing_touchdowns']
    rushing_attempts_against = home_team_info['rushing_attempts_against'] + game_json['away_rushing_attempts']
    rushing_successes_against = home_team_info['rushing_successes_against'] + game_json['away_rushing_successes']
    rushing_percentage_against = rushing_successes_against / rushing_attempts_against
    rushing_touchdowns_against = home_team_info['rushing_touchdowns_against'] + game_json['away_rushing_touchdowns']
    third_down_attempts_against = home_team_info['third_down_attempts_against'] + game_json['away_third_down_attempts']
    third_down_successes_against = home_team_info['third_down_successes_against'] + game_json[
        'away_third_down_successes']
    third_down_percentage_against = third_down_successes_against / third_down_attempts_against
    fourth_down_attempts_against = home_team_info['fourth_down_attempts_against'] + game_json[
        'away_fourth_down_attempts']
    fourth_down_successes_against = home_team_info['fourth_down_successes_against'] + game_json[
        'away_fourth_down_successes']
    fourth_down_percentage_against = fourth_down_successes_against / fourth_down_attempts_against
    two_point_attempts_against = home_team_info['two_point_attempts_against'] + game_json['away_two_point_attempts']
    two_point_successes_against = home_team_info['two_point_successes_against'] + game_json['away_two_point_successes']
    two_point_percentage_against = two_point_successes_against / two_point_attempts_against
    onside_kick_attempts_against = home_team_info['onside_kick_attempts_against'] + game_json[
        'away_onside_kick_attempts']
    onside_kick_successes_against = home_team_info['onside_kick_successes_against'] + game_json[
        'away_onside_kick_successes']
    onside_kick_percentage_against = onside_kick_successes_against / onside_kick_attempts_against
    turnovers_forced = home_team_info['turnovers_forced'] + game_json['away_turnovers']
    fumbles_forced = home_team_info['fumbles_forced'] + game_json['away_fumbles']
    interceptions_forced = home_team_info['interceptions_forced'] + game_json['away_interceptions']
    defensive_touchdowns_against = home_team_info['defensive_touchdowns_against'] + game_json[
        'away_defensive_touchdowns']
    scoop_and_scores_against = home_team_info['scoop_and_scores_against'] + game_json['away_scoop_and_scores']
    pick_sixes_against = home_team_info['pick_sixes_against'] + game_json['away_pick_sixes']
    blocked_field_goals = home_team_info['blocked_field_goals'] + game_json['home_blocked_field_goals']
    blocked_field_goals_against = home_team_info['blocked_field_goals_against'] + game_json['away_blocked_field_goals']
    kick_sixes = home_team_info['kick_sixes'] + game_json['home_kick_sixes']
    kick_sixes_against = home_team_info['kick_sixes_against'] + game_json['away_kick_sixes']
    pat_attempts = home_team_info['pat_attempts'] + game_json['home_pat_attempts']
    pat_successes = home_team_info['pat_successes'] + game_json['home_pat_successes']
    pat_percentage = pat_successes / pat_attempts
    pat_two_point_return = home_team_info['pat_two_point_return'] + game_json['home_pat_two_point_return']
    pat_attempts_against = home_team_info['pat_attempts_against'] + game_json['away_pat_attempts']
    pat_successes_against = home_team_info['pat_successes_against'] + game_json['away_pat_successes']
    pat_percentage_against = pat_successes_against / pat_attempts_against
    pat_two_point_return_against = home_team_info['pat_two_point_return_against'] + game_json[
        'away_pat_two_point_return']
    total_punts = home_team_info['total_punts'] + game_json['home_total_punts']
    total_punts_against = home_team_info['total_punts_against'] + game_json['away_total_punts']
    if game_json['home_longest_punt'] > home_team_info['longest_punt']:
        longest_punt = game_json['home_longest_punt']
    else:
        longest_punt = home_team_info['longest_punt']
    if game_json['away_longest_punt'] > home_team_info['longest_punt_against']:
        longest_punt_against = game_json['away_longest_punt']
    else:
        longest_punt_against = home_team_info['longest_punt_against']
    punt_touchbacks = home_team_info['punt_touchbacks'] + game_json['home_punt_touchbacks']
    punt_touchbacks_against = home_team_info['punt_touchbacks_against'] + game_json['away_punt_touchbacks']
    punt_return_touchdowns = home_team_info['punt_return_touchdowns'] + game_json['home_punt_return_touchdowns']
    punt_return_touchdowns_against = home_team_info['punt_return_touchdowns_against'] + game_json[
        'away_punt_return_touchdowns']
    muffed_punts_recovered = home_team_info['muffed_punts_recovered'] + game_json['home_muffed_punts_recovered']
    muffed_punts_recovered_against = home_team_info['muffed_punts_recovered_against'] + game_json[
        'away_muffed_punts_recovered']
    kickoffs = home_team_info['kickoffs'] + game_json['home_kickoffs']
    kickoffs_against = home_team_info['kickoffs_against'] + game_json['away_kickoffs']
    kickoff_touchbacks = home_team_info['kickoff_touchbacks'] + game_json['home_kickoff_touchbacks']
    kickoff_touchbacks_against = home_team_info['kickoff_touchbacks_against'] + game_json['away_kickoff_touchbacks']
    kickoff_muff_recoveries = home_team_info['kickoff_muff_recoveries'] + game_json['home_kickoff_muff_recoveries']
    kickoff_muff_recoveries_against = home_team_info['kickoff_muff_recoveries_against'] + game_json[
        'away_kickoff_muff_recoveries']

    if game_json['home_score'] > game_json['away_score']:
        current_wins = home_team_info['current_wins'] + 1
        overall_wins = home_team_info['overall_wins'] + 1
        current_losses = home_team_info['current_losses']
        overall_losses = home_team_info['overall_losses']
        if is_conference_game:
            current_conference_wins = home_team_info['current_conference_wins'] + 1
            current_conference_losses = home_team_info['current_conference_losses']
            overall_conference_wins = home_team_info['overall_conference_wins'] + 1
            overall_conference_losses = home_team_info['overall_conference_losses']
        else:
            current_conference_wins = home_team_info['current_conference_wins']
            current_conference_losses = home_team_info['current_conference_losses']
            overall_conference_wins = home_team_info['overall_conference_wins']
            overall_conference_losses = home_team_info['overall_conference_losses']
    else:
        current_wins = home_team_info['current_wins']
        overall_wins = home_team_info['overall_wins']
        current_losses = home_team_info['current_losses'] + 1
        overall_losses = home_team_info['overall_losses'] + 1
        if is_conference_game:
            current_conference_wins = home_team_info['current_conference_wins']
            current_conference_losses = home_team_info['current_conference_losses'] + 1
            overall_conference_wins = home_team_info['overall_conference_wins']
            overall_conference_losses = home_team_info['overall_conference_losses'] + 1
        else:
            current_conference_wins = home_team_info['current_conference_wins']
            current_conference_losses = home_team_info['current_conference_losses']
            overall_conference_wins = home_team_info['overall_conference_wins']
            overall_conference_losses = home_team_info['overall_conference_losses']

    num_games = current_wins + current_losses
    average_diff_on_offense = game_json['home_average_diff_on_offense'] + \
                              (num_games * home_team_info['average_diff_on_offense']) / (num_games + 1)
    average_diff_on_defense = game_json['home_average_diff_on_defense'] + \
                              (num_games * home_team_info['average_diff_on_defense']) / (num_games + 1)
    average_punt = game_json['home_average_punt'] + \
                   (num_games * home_team_info['average_punt']) / (num_games + 1)
    average_punt_against = game_json['away_average_punt'] + \
                           (num_games * home_team_info['average_punt_against']) / (num_games + 1)

    home_team_stats = {
        'num_plays': num_plays,
        'total_yards': total_yards,
        'passing_yards': passing_yards,
        'rushing_yards': rushing_yards,
        'time_of_possession': time_of_possession,
        'average_diff_on_offense': average_diff_on_offense,
        'average_diff_on_defense': average_diff_on_defense,
        'field_goal_attempts': field_goal_attempts,
        'field_goal_makes': field_goal_makes,
        'field_goal_percentage': field_goal_percentage,
        'longest_field_goal': longest_field_goal,
        'longest_touchdown': longest_touchdown,
        'passing_attempts': passing_attempts,
        'passing_completions': passing_completions,
        'passing_percentage': passing_percentage,
        'passing_touchdowns': passing_touchdowns,
        'rushing_attempts': rushing_attempts,
        'rushing_successes': rushing_successes,
        'rushing_percentage': rushing_percentage,
        'rushing_touchdowns': rushing_touchdowns,
        'third_down_attempts': third_down_attempts,
        'third_down_successes': third_down_successes,
        'third_down_percentage': third_down_percentage,
        'fourth_down_attempts': fourth_down_attempts,
        'fourth_down_successes': fourth_down_successes,
        'fourth_down_percentage': fourth_down_percentage,
        'two_point_attempts': two_point_attempts,
        'two_point_successes': two_point_successes,
        'two_point_percentage': two_point_percentage,
        'onside_kick_attempts': onside_kick_attempts,
        'onside_kick_successes': onside_kick_successes,
        'onside_kick_percentage': onside_kick_percentage,
        'offensive_plays': offensive_plays,
        'defensive_plays': defensive_plays,
        'turnovers': turnovers,
        'fumbles': fumbles,
        'interceptions': interceptions,
        'defensive_touchdowns': defensive_touchdowns,
        'scoop_and_scores': scoop_and_scores,
        'pick_sixes': pick_sixes,
        'kickoff_defensive_touchdowns': kickoff_defensive_touchdowns,
        'safeties_forced': safeties_forced,
        'safeties_allowed': safeties_allowed,
        'passing_yards_against': passing_yards_against,
        'rushing_yards_against': rushing_yards_against,
        'time_of_possession_against': time_of_possession_against,
        'field_goal_attempts_against': field_goal_attempts_against,
        'field_goal_makes_against': field_goal_makes_against,
        'field_goal_percentage_against': field_goal_percentage_against,
        'longest_field_goal_against': longest_field_goal_against,
        'longest_touchdown_against': longest_touchdown_against,
        'passing_attempts_against': passing_attempts_against,
        'passing_completions_against': passing_completions_against,
        'passing_percentage_against': passing_percentage_against,
        'passing_touchdowns_against': passing_touchdowns_against,
        'rushing_attempts_against': rushing_attempts_against,
        'rushing_successes_against': rushing_successes_against,
        'rushing_percentage_against': rushing_percentage_against,
        'rushing_touchdowns_against': rushing_touchdowns_against,
        'third_down_attempts_against': third_down_attempts_against,
        'third_down_successes_against': third_down_successes_against,
        'third_down_percentage_against': third_down_percentage_against,
        'fourth_down_attempts_against': fourth_down_attempts_against,
        'fourth_down_successes_against': fourth_down_successes_against,
        'fourth_down_percentage_against': fourth_down_percentage_against,
        'two_point_attempts_against': two_point_attempts_against,
        'two_point_successes_against': two_point_successes_against,
        'two_point_percentage_against': two_point_percentage_against,
        'onside_kick_attempts_against': onside_kick_attempts_against,
        'onside_kick_successes_against': onside_kick_successes_against,
        'onside_kick_percentage_against': onside_kick_percentage_against,
        'turnovers_forced': turnovers_forced,
        'fumbles_forced': fumbles_forced,
        'interceptions_forced': interceptions_forced,
        'defensive_touchdowns_against': defensive_touchdowns_against,
        'scoop_and_scores_against': scoop_and_scores_against,
        'pick_sixes_against': pick_sixes_against,
        'blocked_field_goals': blocked_field_goals,
        'blocked_field_goals_against': blocked_field_goals_against,
        'kick_sixes': kick_sixes,
        'kick_sixes_against': kick_sixes_against,
        'pat_attempts': pat_attempts,
        'pat_successes': pat_successes,
        'pat_percentage': pat_percentage,
        'pat_two_point_return': pat_two_point_return,
        'pat_attempts_against': pat_attempts_against,
        'pat_successes_against': pat_successes_against,
        'pat_percentage_against': pat_percentage_against,
        'pat_two_point_return_against': pat_two_point_return_against,
        'total_punts': total_punts,
        'total_punts_against': total_punts_against,
        'longest_punt': longest_punt,
        'longest_punt_against': longest_punt_against,
        'average_punt': average_punt,
        'average_punt_against': average_punt_against,
        'punt_touchbacks': punt_touchbacks,
        'punt_touchbacks_against': punt_touchbacks_against,
        'punt_return_touchdowns': punt_return_touchdowns,
        'punt_return_touchdowns_against': punt_return_touchdowns_against,
        'muffed_punts_recovered': muffed_punts_recovered,
        'muffed_punts_recovered_against': muffed_punts_recovered_against,
        'kickoffs': kickoffs,
        'kickoffs_against': kickoffs_against,
        'kickoff_touchbacks': kickoff_touchbacks,
        'kickoff_touchbacks_against': kickoff_touchbacks_against,
        'kickoff_muff_recoveries': kickoff_muff_recoveries,
        'kickoff_muff_recoveries_against': kickoff_muff_recoveries_against,
        'current_wins': current_wins,
        'overall_wins': overall_wins,
        'current_losses': current_losses,
        'overall_losses': overall_losses,
        'current_conference_wins': current_conference_wins,
        'current_conference_losses': current_conference_losses,
        'overall_conference_wins': overall_conference_wins,
        'overall_conference_losses': overall_conference_losses
    }

    num_plays = away_team_info['num_plays'] + game_json['num_plays']
    total_yards = away_team_info['total_yards'] + game_json['away_total_yards']
    passing_yards = away_team_info['passing_yards'] + game_json['away_passing_yards']
    rushing_yards = away_team_info['rushing_yards'] + game_json['away_rushing_yards']
    # Convert TOP to seconds, add, then convert back to string
    minutes = game_json['away_time_of_possession'].split(":")[0]
    seconds = game_json['away_time_of_possession'].split(":")[1]
    game_top = int(minutes) * 60 + int(seconds)
    minutes = away_team_info['time_of_possession'].split(":")[0]
    seconds = away_team_info['time_of_possession'].split(":")[1]
    current_total_top = int(minutes) * 60 + int(seconds)
    total_top = current_total_top + game_top
    minutes = str(int(total_top / 60))
    seconds = str(total_top % 60)
    time_of_possession = minutes + ":" + seconds
    field_goal_attempts = away_team_info['field_goal_attempts'] + game_json['away_field_goal_attempts']
    field_goal_makes = away_team_info['field_goal_makes'] + game_json['away_field_goal_makes']
    field_goal_percentage = field_goal_makes / field_goal_attempts

    if game_json['away_longest_field_goal'] > away_team_info['longest_field_goal']:
        longest_field_goal = game_json['away_longest_field_goal']
    else:
        longest_field_goal = away_team_info['longest_field_goal']

    if game_json['away_longest_touchdown'] > away_team_info['longest_touchdown']:
        longest_touchdown = game_json['away_longest_touchdown']
    else:
        longest_touchdown = away_team_info['longest_touchdown']

    passing_attempts = away_team_info['passing_attempts'] + game_json['away_passing_attempts']
    passing_completions = away_team_info['passing_completions'] + game_json['away_passing_completions']
    passing_percentage = passing_completions / passing_attempts
    passing_touchdowns = away_team_info['passing_touchdowns'] + game_json['away_passing_touchdowns']
    rushing_attempts = away_team_info['rushing_attempts'] + game_json['away_rushing_attempts']
    rushing_successes = away_team_info['rushing_successes'] + game_json['away_rushing_successes']
    rushing_percentage = rushing_successes / rushing_attempts
    rushing_touchdowns = away_team_info['rushing_touchdowns'] + game_json['away_rushing_touchdowns']
    third_down_attempts = away_team_info['third_down_attempts'] + game_json['away_third_down_attempts']
    third_down_successes = away_team_info['third_down_successes'] + game_json['away_third_down_successes']
    third_down_percentage = third_down_successes / third_down_attempts
    fourth_down_attempts = away_team_info['fourth_down_attempts'] + game_json['away_fourth_down_attempts']
    fourth_down_successes = away_team_info['fourth_down_successes'] + game_json['away_fourth_down_successes']
    fourth_down_percentage = fourth_down_successes / fourth_down_attempts
    two_point_attempts = away_team_info['two_point_attempts'] + game_json['away_two_point_attempts']
    two_point_successes = away_team_info['two_point_successes'] + game_json['away_two_point_successes']
    two_point_percentage = two_point_successes / two_point_attempts
    onside_kick_attempts = away_team_info['onside_kick_attempts'] + game_json['away_onside_kick_attempts']
    onside_kick_successes = away_team_info['onside_kick_successes'] + game_json['away_onside_kick_successes']
    onside_kick_percentage = onside_kick_successes / onside_kick_attempts
    offensive_plays = away_team_info['offensive_plays'] + game_json['away_offensive_plays']
    defensive_plays = away_team_info['defensive_plays'] + game_json['away_defensive_plays']
    turnovers = away_team_info['turnovers'] + game_json['away_turnovers']
    fumbles = away_team_info['fumbles'] + game_json['away_fumbles']
    interceptions = away_team_info['interceptions'] + game_json['away_interceptions']
    defensive_touchdowns = away_team_info['defensive_touchdowns'] + game_json['away_defensive_touchdowns']
    scoop_and_scores = away_team_info['scoop_and_scores'] + game_json['away_scoop_and_scores']
    pick_sixes = away_team_info['pick_sixes'] + game_json['away_pick_sixes']
    kickoff_defensive_touchdowns = away_team_info['kickoff_defensive_touchdowns'] + game_json[
        'away_kickoff_defensive_touchdowns']
    safeties_forced = away_team_info['safeties_forced'] + game_json['away_safeties_forced']
    safeties_allowed = away_team_info['safeties_allowed'] + game_json['home_safeties_forced']
    passing_yards_against = away_team_info['passing_yards_against'] + game_json['home_passing_yards']
    rushing_yards_against = away_team_info['rushing_yards_against'] + game_json['home_rushing_yards']
    # Convert TOP to seconds, add, then convert back to string
    minutes = game_json['home_time_of_possession'].split(":")[0]
    seconds = game_json['home_time_of_possession'].split(":")[1]
    game_top = int(minutes) * 60 + int(seconds)
    minutes = away_team_info['time_of_possession_against'].split(":")[0]
    seconds = away_team_info['time_of_possession_against'].split(":")[1]
    current_total_top = int(minutes) * 60 + int(seconds)
    total_top = current_total_top + game_top
    minutes = str(int(total_top / 60))
    seconds = str(total_top % 60)
    time_of_possession_against = minutes + ":" + seconds
    field_goal_attempts_against = away_team_info['field_goal_attempts_against'] + game_json['home_field_goal_attempts']
    field_goal_makes_against = away_team_info['field_goal_makes_against'] + game_json['home_field_goal_successes']
    field_goal_percentage_against = field_goal_makes_against / field_goal_attempts_against
    if game_json['home_longest_field_goal'] > away_team_info['longest_field_goal_against']:
        longest_field_goal_against = game_json['home_longest_field_goal']
    else:
        longest_field_goal_against = away_team_info['longest_field_goal_against']
    if game_json['home_longest_touchdown'] > away_team_info['longest_touchdown_against']:
        longest_touchdown_against = game_json['home_longest_touchdown']
    else:
        longest_touchdown_against = away_team_info['longest_touchdown_against']
    passing_attempts_against = away_team_info['passing_attempts_against'] + game_json['home_passing_attempts']
    passing_completions_against = away_team_info['passing_completions_against'] + game_json['home_passing_completions']
    passing_percentage_against = passing_completions_against / passing_attempts_against
    passing_touchdowns_against = away_team_info['passing_touchdowns_against'] + game_json['home_passing_touchdowns']
    rushing_attempts_against = away_team_info['rushing_attempts_against'] + game_json['home_rushing_attempts']
    rushing_successes_against = away_team_info['rushing_successes_against'] + game_json['home_rushing_successes']
    rushing_percentage_against = rushing_successes_against / rushing_attempts_against
    rushing_touchdowns_against = away_team_info['rushing_touchdowns_against'] + game_json['home_rushing_touchdowns']
    third_down_attempts_against = away_team_info['third_down_attempts_against'] + game_json['home_third_down_attempts']
    third_down_successes_against = away_team_info['third_down_successes_against'] + game_json[
        'home_third_down_successes']
    third_down_percentage_against = third_down_successes_against / third_down_attempts_against
    fourth_down_attempts_against = away_team_info['fourth_down_attempts_against'] + game_json[
        'home_fourth_down_attempts']
    fourth_down_successes_against = away_team_info['fourth_down_successes_against'] + game_json[
        'home_fourth_down_successes']
    fourth_down_percentage_against = fourth_down_successes_against / fourth_down_attempts_against
    two_point_attempts_against = away_team_info['two_point_attempts_against'] + game_json['home_two_point_attempts']
    two_point_successes_against = away_team_info['two_point_successes_against'] + game_json['home_two_point_successes']
    two_point_percentage_against = two_point_successes_against / two_point_attempts_against
    onside_kick_attempts_against = away_team_info['onside_kick_attempts_against'] + game_json[
        'home_onside_kick_attempts']
    onside_kick_successes_against = away_team_info['onside_kick_successes_against'] + game_json[
        'home_onside_kick_successes']
    onside_kick_percentage_against = onside_kick_successes_against / onside_kick_attempts_against
    turnovers_forced = away_team_info['turnovers_forced'] + game_json['home_turnovers']
    fumbles_forced = away_team_info['fumbles_forced'] + game_json['home_fumbles']
    interceptions_forced = away_team_info['interceptions_forced'] + game_json['home_interceptions']
    defensive_touchdowns_against = away_team_info['defensive_touchdowns_against'] + game_json[
        'home_defensive_touchdowns']
    scoop_and_scores_against = away_team_info['scoop_and_scores_against'] + game_json['home_scoop_and_scores']
    pick_sixes_against = away_team_info['pick_sixes_against'] + game_json['home_pick_sixes']
    blocked_field_goals = away_team_info['blocked_field_goals'] + game_json['away_blocked_field_goals']
    blocked_field_goals_against = away_team_info['blocked_field_goals_against'] + game_json['home_blocked_field_goals']
    kick_sixes = away_team_info['kick_sixes'] + game_json['away_kick_sixes']
    kick_sixes_against = away_team_info['kick_sixes_against'] + game_json['home_kick_sixes']
    pat_attempts = away_team_info['pat_attempts'] + game_json['away_pat_attempts']
    pat_successes = away_team_info['pat_successes'] + game_json['away_pat_successes']
    pat_percentage = pat_successes / pat_attempts
    pat_two_point_return = away_team_info['pat_two_point_return'] + game_json['away_pat_two_point_return']
    pat_attempts_against = away_team_info['pat_attempts_against'] + game_json['home_pat_attempts']
    pat_successes_against = away_team_info['pat_successes_against'] + game_json['home_pat_successes']
    pat_percentage_against = pat_successes_against / pat_attempts_against
    pat_two_point_return_against = away_team_info['pat_two_point_return_against'] + game_json[
        'home_pat_two_point_return']
    total_punts = away_team_info['total_punts'] + game_json['away_total_punts']
    total_punts_against = away_team_info['total_punts_against'] + game_json['home_total_punts']
    if game_json['away_longest_punt'] > away_team_info['longest_punt']:
        longest_punt = game_json['away_longest_punt']
    else:
        longest_punt = away_team_info['longest_punt']
    if game_json['home_longest_punt'] > away_team_info['longest_punt_against']:
        longest_punt_against = game_json['home_longest_punt']
    else:
        longest_punt_against = away_team_info['longest_punt_against']
    punt_touchbacks = away_team_info['punt_touchbacks'] + game_json['away_punt_touchbacks']
    punt_touchbacks_against = away_team_info['punt_touchbacks_against'] + game_json['home_punt_touchbacks']
    punt_return_touchdowns = away_team_info['punt_return_touchdowns'] + game_json['away_punt_return_touchdowns']
    punt_return_touchdowns_against = away_team_info['punt_return_touchdowns_against'] + game_json[
        'home_punt_return_touchdowns']
    muffed_punts_recovered = away_team_info['muffed_punts_recovered'] + game_json['away_muffed_punts_recovered']
    muffed_punts_recovered_against = away_team_info['muffed_punts_recovered_against'] + game_json[
        'home_muffed_punts_recovered']
    kickoffs = away_team_info['kickoffs'] + game_json['away_kickoffs']
    kickoffs_against = away_team_info['kickoffs_against'] + game_json['home_kickoffs']
    kickoff_touchbacks = away_team_info['kickoff_touchbacks'] + game_json['away_kickoff_touchbacks']
    kickoff_touchbacks_against = away_team_info['kickoff_touchbacks_against'] + game_json['home_kickoff_touchbacks']
    kickoff_muff_recoveries = away_team_info['kickoff_muff_recoveries'] + game_json['away_kickoff_muff_recoveries']
    kickoff_muff_recoveries_against = away_team_info['kickoff_muff_recoveries_against'] + game_json[
        'home_kickoff_muff_recoveries']

    if game_json['away_score'] > game_json['home_score']:
        current_wins = away_team_info['current_wins'] + 1
        overall_wins = away_team_info['overall_wins'] + 1
        current_losses = away_team_info['current_losses']
        overall_losses = away_team_info['overall_losses']
        if is_conference_game:
            current_conference_wins = away_team_info['current_conference_wins'] + 1
            current_conference_losses = away_team_info['current_conference_losses']
            overall_conference_wins = away_team_info['overall_conference_wins'] + 1
            overall_conference_losses = away_team_info['overall_conference_losses']
        else:
            current_conference_wins = away_team_info['current_conference_wins']
            current_conference_losses = away_team_info['current_conference_losses']
            overall_conference_wins = away_team_info['overall_conference_wins']
            overall_conference_losses = away_team_info['overall_conference_losses']
    else:
        current_wins = away_team_info['current_wins']
        overall_wins = away_team_info['overall_wins']
        current_losses = away_team_info['current_losses'] + 1
        overall_losses = away_team_info['overall_losses'] + 1
        if is_conference_game:
            current_conference_wins = away_team_info['current_conference_wins']
            current_conference_losses = away_team_info['current_conference_losses'] + 1
            overall_conference_wins = away_team_info['overall_conference_wins']
            overall_conference_losses = away_team_info['overall_conference_losses'] + 1
        else:
            current_conference_wins = away_team_info['current_conference_wins']
            current_conference_losses = away_team_info['current_conference_losses']
            overall_conference_wins = away_team_info['overall_conference_wins']
            overall_conference_losses = away_team_info['overall_conference_losses']

    num_games = current_wins + current_losses
    average_diff_on_offense = game_json['away_average_diff_on_offense'] + \
                              (num_games * away_team_info['average_diff_on_offense']) / (num_games + 1)
    average_diff_on_defense = game_json['away_average_diff_on_defense'] + \
                              (num_games * away_team_info['average_diff_on_defense']) / (num_games + 1)
    average_punt = game_json['away_average_punt'] + \
                   (num_games * away_team_info['average_punt']) / (num_games + 1)
    average_punt_against = game_json['home_average_punt'] + \
                           (num_games * away_team_info['average_punt_against']) / (num_games + 1)

    away_team_stats = {
        'num_plays': num_plays,
        'total_yards': total_yards,
        'passing_yards': passing_yards,
        'rushing_yards': rushing_yards,
        'time_of_possession': time_of_possession,
        'average_diff_on_offense': average_diff_on_offense,
        'average_diff_on_defense': average_diff_on_defense,
        'field_goal_attempts': field_goal_attempts,
        'field_goal_makes': field_goal_makes,
        'field_goal_percentage': field_goal_percentage,
        'longest_field_goal': longest_field_goal,
        'longest_touchdown': longest_touchdown,
        'passing_attempts': passing_attempts,
        'passing_completions': passing_completions,
        'passing_percentage': passing_percentage,
        'passing_touchdowns': passing_touchdowns,
        'rushing_attempts': rushing_attempts,
        'rushing_successes': rushing_successes,
        'rushing_percentage': rushing_percentage,
        'rushing_touchdowns': rushing_touchdowns,
        'third_down_attempts': third_down_attempts,
        'third_down_successes': third_down_successes,
        'third_down_percentage': third_down_percentage,
        'fourth_down_attempts': fourth_down_attempts,
        'fourth_down_successes': fourth_down_successes,
        'fourth_down_percentage': fourth_down_percentage,
        'two_point_attempts': two_point_attempts,
        'two_point_successes': two_point_successes,
        'two_point_percentage': two_point_percentage,
        'onside_kick_attempts': onside_kick_attempts,
        'onside_kick_successes': onside_kick_successes,
        'onside_kick_percentage': onside_kick_percentage,
        'offensive_plays': offensive_plays,
        'defensive_plays': defensive_plays,
        'turnovers': turnovers,
        'fumbles': fumbles,
        'interceptions': interceptions,
        'defensive_touchdowns': defensive_touchdowns,
        'scoop_and_scores': scoop_and_scores,
        'pick_sixes': pick_sixes,
        'kickoff_defensive_touchdowns': kickoff_defensive_touchdowns,
        'safeties_forced': safeties_forced,
        'safeties_allowed': safeties_allowed,
        'passing_yards_against': passing_yards_against,
        'rushing_yards_against': rushing_yards_against,
        'time_of_possession_against': time_of_possession_against,
        'field_goal_attempts_against': field_goal_attempts_against,
        'field_goal_makes_against': field_goal_makes_against,
        'field_goal_percentage_against': field_goal_percentage_against,
        'longest_field_goal_against': longest_field_goal_against,
        'longest_touchdown_against': longest_touchdown_against,
        'passing_attempts_against': passing_attempts_against,
        'passing_completions_against': passing_completions_against,
        'passing_percentage_against': passing_percentage_against,
        'passing_touchdowns_against': passing_touchdowns_against,
        'rushing_attempts_against': rushing_attempts_against,
        'rushing_successes_against': rushing_successes_against,
        'rushing_percentage_against': rushing_percentage_against,
        'rushing_touchdowns_against': rushing_touchdowns_against,
        'third_down_attempts_against': third_down_attempts_against,
        'third_down_successes_against': third_down_successes_against,
        'third_down_percentage_against': third_down_percentage_against,
        'fourth_down_attempts_against': fourth_down_attempts_against,
        'fourth_down_successes_against': fourth_down_successes_against,
        'fourth_down_percentage_against': fourth_down_percentage_against,
        'two_point_attempts_against': two_point_attempts_against,
        'two_point_successes_against': two_point_successes_against,
        'two_point_percentage_against': two_point_percentage_against,
        'onside_kick_attempts_against': onside_kick_attempts_against,
        'onside_kick_successes_against': onside_kick_successes_against,
        'onside_kick_percentage_against': onside_kick_percentage_against,
        'turnovers_forced': turnovers_forced,
        'fumbles_forced': fumbles_forced,
        'interceptions_forced': interceptions_forced,
        'defensive_touchdowns_against': defensive_touchdowns_against,
        'scoop_and_scores_against': scoop_and_scores_against,
        'pick_sixes_against': pick_sixes_against,
        'blocked_field_goals': blocked_field_goals,
        'blocked_field_goals_against': blocked_field_goals_against,
        'kick_sixes': kick_sixes,
        'kick_sixes_against': kick_sixes_against,
        'pat_attempts': pat_attempts,
        'pat_successes': pat_successes,
        'pat_percentage': pat_percentage,
        'pat_two_point_return': pat_two_point_return,
        'pat_attempts_against': pat_attempts_against,
        'pat_successes_against': pat_successes_against,
        'pat_percentage_against': pat_percentage_against,
        'pat_two_point_return_against': pat_two_point_return_against,
        'total_punts': total_punts,
        'total_punts_against': total_punts_against,
        'longest_punt': longest_punt,
        'longest_punt_against': longest_punt_against,
        'average_punt': average_punt,
        'average_punt_against': average_punt_against,
        'punt_touchbacks': punt_touchbacks,
        'punt_touchbacks_against': punt_touchbacks_against,
        'punt_return_touchdowns': punt_return_touchdowns,
        'punt_return_touchdowns_against': punt_return_touchdowns_against,
        'muffed_punts_recovered': muffed_punts_recovered,
        'muffed_punts_recovered_against': muffed_punts_recovered_against,
        'kickoffs': kickoffs,
        'kickoffs_against': kickoffs_against,
        'kickoff_touchbacks': kickoff_touchbacks,
        'kickoff_touchbacks_against': kickoff_touchbacks_against,
        'kickoff_muff_recoveries': kickoff_muff_recoveries,
        'kickoff_muff_recoveries_against': kickoff_muff_recoveries_against,
        'current_wins': current_wins,
        'overall_wins': overall_wins,
        'current_losses': current_losses,
        'overall_losses': overall_losses,
        'current_conference_wins': current_conference_wins,
        'current_conference_losses': current_conference_losses,
        'overall_conference_wins': overall_conference_wins,
        'overall_conference_losses': overall_conference_losses
    }

    return home_team_stats, away_team_stats
