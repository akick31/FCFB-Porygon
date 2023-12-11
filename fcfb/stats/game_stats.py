def calculate_game_stats(plays, team_stats, playclock):
    """
    Calculate the game stats from the plays

    :param plays:
    :param team_stats:
    :param playclock:
    :return:
    """

    # Gather the stats from the plays
    home_total_diff_on_offense = 0
    home_total_diff_on_defense = 0
    away_total_diff_on_offense = 0
    away_total_diff_on_defense = 0
    home_field_goal_attempts = 0
    home_field_goals_made = 0
    home_field_goal_percentage = 0
    away_field_goal_attempts = 0
    away_field_goals_made = 0
    away_field_goal_percentage = 0
    home_longest_field_goal = 0
    away_longest_field_goal = 0
    home_longest_touchdown = 0
    away_longest_touchdown = 0
    home_passing_attempts = 0
    home_passing_completions = 0
    home_passing_percentage = 0
    away_passing_attempts = 0
    away_passing_completions = 0
    away_passing_percentage = 0
    home_rushing_attempts = 0
    home_rushing_successes = 0
    home_rushing_percentage = 0
    away_rushing_attempts = 0
    away_rushing_successes = 0
    away_rushing_percentage = 0
    home_third_down_attempts = 0
    home_third_down_successes = 0
    home_third_down_percentage = 0
    away_third_down_attempts = 0
    away_third_down_successes = 0
    away_third_down_percentage = 0
    home_fourth_down_attempts = 0
    home_fourth_down_successes = 0
    home_fourth_down_percentage = 0
    away_fourth_down_attempts = 0
    away_fourth_down_successes = 0
    away_fourth_down_percentage = 0
    home_two_point_attempts = 0
    home_two_point_successes = 0
    home_two_point_percentage = 0
    away_two_point_attempts = 0
    away_two_point_successes = 0
    away_two_point_percentage = 0
    home_onside_kick_attempts = 0
    home_onside_kick_successes = 0
    home_onside_kick_percentage = 0
    away_onside_kick_attempts = 0
    away_onside_kick_successes = 0
    away_onside_kick_percentage = 0
    home_total_plays = 0
    home_offensive_plays = 0
    home_defensive_plays = 0
    away_total_plays = 0
    away_offensive_plays = 0
    away_defensive_plays = 0
    home_turnovers = 0
    home_fumbles = 0
    home_interceptions = 0
    away_turnovers = 0
    away_fumbles = 0
    away_interceptions = 0
    home_defensive_touchdowns = 0
    home_scoop_and_scores = 0
    home_pick_sixes = 0
    home_kickoff_defensive_touchdowns = 0
    away_defensive_touchdowns = 0
    away_scoop_and_scores = 0
    away_pick_sixes = 0
    away_kickoff_defensive_touchdowns = 0
    home_kick_return_touchdowns = 0
    away_kick_return_touchdowns = 0

    for play in plays:
        if play["Ball Location"] == "":
            ball_location = 0
        else:
            ball_location = int(play["Ball Location"])
        possession = play["Possession"]
        down = play["Down"]
        if play["Yards to go"] == "":
            yards_to_go = 0
        else:
            yards_to_go = int(play["Yards to go"])
        if play["Defensive number"] == "":
            continue
        else:
            defensive_number = int(play["Defensive number"])
        if play["Offensive number"] == "":
            continue
        else:
            offensive_number = int(play["Offensive number"])
        play_type = play["Play"]
        result = play["Result"]
        actual_result = play["Actual result"]
        if play["Yards"] == "":
            yards = 0
        else:
            yards = int(play["Yards"])

        difference = abs(1500 - offensive_number + defensive_number) if offensive_number - defensive_number > 750 else abs(offensive_number - defensive_number)
        if possession == "home":
            home_total_diff_on_offense += difference
            home_offensive_plays += 1
            away_total_diff_on_defense += difference
            away_defensive_plays += 1
        else:
            away_total_diff_on_offense += difference
            away_offensive_plays += 1
            home_total_diff_on_defense += difference
            home_defensive_plays += 1

        # Calculate field goal stats
        if play_type == "FIELD_GOAL":
            field_goal_distance = int(ball_location) - 17
            if possession == "home":
                home_field_goal_attempts += 1
                if result == "FIELD_GOAL":
                    home_field_goals_made += 1
                    if field_goal_distance > home_longest_field_goal:
                        home_longest_field_goal = field_goal_distance
                home_field_goal_percentage = home_field_goals_made/home_field_goal_attempts
            else:
                away_field_goal_attempts += 1
                if result == "FIELD_GOAL":
                    away_field_goals_made += 1
                    if field_goal_distance > away_longest_field_goal:
                        away_longest_field_goal = field_goal_distance
                away_field_goal_percentage = away_field_goals_made/away_field_goal_attempts

        # Calculate passing stats
        elif play_type == "PASS":
            if possession == "home":
                home_passing_attempts += 1
                if result == "GAIN":
                    home_passing_completions += 1
                if result == "TURNOVER":
                    home_interceptions += 1
                    home_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    home_interceptions += 1
                    home_turnovers += 1
                    away_pick_sixes += 1
                    away_defensive_touchdowns += 1
                home_passing_percentage = home_passing_completions/home_passing_attempts
            else:
                away_passing_attempts += 1
                if result == "GAIN":
                    away_passing_completions += 1
                if result == "TURNOVER":
                    away_interceptions += 1
                    away_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    away_interceptions += 1
                    away_turnovers += 1
                    home_pick_sixes += 1
                    home_defensive_touchdowns += 1
                away_passing_percentage = away_passing_completions/away_passing_attempts

        # Calculate rushing stats
        elif play_type == "RUN":
            if possession == "home":
                home_rushing_attempts += 1
                if down == "1" and yards >= 5:
                    home_rushing_successes += 1
                elif down == "2" and yards/yards_to_go >= 0.7:
                    home_rushing_successes += 1
                elif (down == "3" or down == "4") and yards >= yards_to_go:
                    home_rushing_successes += 1
                if result == "TURNOVER":
                    home_fumbles += 1
                    home_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    home_fumbles += 1
                    home_turnovers += 1
                    away_scoop_and_scores += 1
                    away_defensive_touchdowns += 1
                home_rushing_percentage = home_rushing_successes/home_rushing_attempts
            else:
                away_rushing_attempts += 1
                if down == "1" and yards >= 5:
                    home_rushing_successes += 1
                elif down == "2" and yards/yards_to_go >= 0.7:
                    home_rushing_successes += 1
                elif (down == "3" or down == "4") and yards >= yards_to_go:
                    home_rushing_successes += 1
                if result == "TURNOVER":
                    away_fumbles += 1
                    away_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    away_fumbles += 1
                    away_turnovers += 1
                    home_scoop_and_scores += 1
                    home_defensive_touchdowns += 1
                away_rushing_percentage = away_rushing_successes/away_rushing_attempts

        # Calculate onside stats
        elif play_type == "KICKOFF_ONSIDE":
            if possession == "home":
                home_onside_kick_attempts += 1
                if result == "GAIN":
                    home_onside_kick_successes += 1
                if result == "TOUCHDOWN":
                    home_onside_kick_successes += 1
                    home_kick_return_touchdowns += 1
                if result == "TURNOVER_TOUCHDOWN":
                    away_kickoff_defensive_touchdowns += 1
                    away_defensive_touchdowns += 1
            else:
                away_onside_kick_attempts += 1
                if result == "GAIN":
                    away_onside_kick_successes += 1
                if result == "TOUCHDOWN":
                    away_onside_kick_successes += 1
                    away_kick_return_touchdowns += 1
                if result == "TURNOVER_TOUCHDOWN":
                    home_kickoff_defensive_touchdowns += 1
                    home_defensive_touchdowns += 1

        elif play_type == "KICKOFF_NORMAL" or play_type == "KICKOFF_SQUIB":
            if possession == "home":
                if result == "TOUCHDOWN":
                    away_kick_return_touchdowns += 1
                if result == "TURNOVER":
                    home_fumbles += 1
                    home_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    home_fumbles += 1
                    home_turnovers += 1
                    away_kickoff_defensive_touchdowns += 1
                    away_defensive_touchdowns += 1
            else:
                if result == "TOUCHDOWN":
                    home_kick_return_touchdowns += 1
                if result == "TURNOVER":
                    away_fumbles += 1
                    away_turnovers += 1
                if result == "TURNOVER_TOUCHDOWN":
                    away_fumbles += 1
                    away_turnovers += 1
                    home_kickoff_defensive_touchdowns += 1
                    home_defensive_touchdowns += 1

        # Calculate two point stats
        elif play_type == "TWO_POINT":
            if possession == "home":
                home_two_point_attempts += 1
                if result == "TWO_POINT":
                    home_two_point_successes += 1
            else:
                away_two_point_attempts += 1
                if result == "TWO_POINT":
                    away_two_point_successes += 1

        if down == "3":
            if possession == "home":
                home_third_down_attempts += 1
                if result == "GAIN" and yards_to_go <= yards:
                    home_third_down_successes += 1
                home_third_down_percentage = home_third_down_successes/home_third_down_attempts
            else:
                away_third_down_attempts += 1
                if result == "GAIN" and yards_to_go <= yards:
                    away_third_down_successes += 1
                away_third_down_percentage = away_third_down_successes/away_third_down_attempts

        if down == "4" and (play_type == "RUN" or play_type == "PASS"):
            if possession == "home":
                home_fourth_down_attempts += 1
                if result == "GAIN" and yards_to_go <= yards:
                    home_fourth_down_successes += 1
                home_fourth_down_percentage = home_fourth_down_successes/home_fourth_down_attempts
            else:
                away_fourth_down_attempts += 1
                if result == "GAIN" and yards_to_go <= yards:
                    away_fourth_down_successes += 1
                away_fourth_down_percentage = away_fourth_down_successes/away_fourth_down_attempts

        if result == "GAIN":
            if actual_result == "TOUCHDOWN":
                if possession == "home":
                    if yards > home_longest_touchdown:
                        home_longest_touchdown = yards
                else:
                    if yards > away_longest_touchdown:
                        away_longest_touchdown = yards

    stats = {"num_plays": len(plays),
             "home_timeouts": team_stats["home_team_stats"]["timeouts"],
             "away_timeouts": team_stats["away_team_stats"]["timeouts"],
             "game_timer": playclock,
             "home_total_yards": team_stats["home_team_stats"]["total_yards"],
             "away_total_yards": team_stats["away_team_stats"]["total_yards"],
             "home_passing_yards": team_stats["home_team_stats"]["total_passing_yards"],
             "away_passing_yards": team_stats["away_team_stats"]["total_passing_yards"],
             "home_rushing_yards": team_stats["home_team_stats"]["total_rushing_yards"],
             "away_rushing_yards": team_stats["away_team_stats"]["total_rushing_yards"],
             "home_time_of_possession": team_stats["home_team_stats"]["time_of_possession"],
             "away_time_of_possession": team_stats["away_team_stats"]["time_of_possession"],
             "home_average_diff_on_offense": home_total_diff_on_offense / home_offensive_plays,
             "away_average_diff_on_offense": away_total_diff_on_offense / away_defensive_plays,
             "home_average_diff_on_defense": home_total_diff_on_defense / home_offensive_plays,
             "away_average_diff_on_defense": away_total_diff_on_defense / away_defensive_plays,
             "home_field_goal_attempts": home_field_goal_attempts,
             "home_field_goal_makes": home_field_goals_made,
             "home_field_goal_percentage": home_field_goal_percentage,
             "away_field_goal_attempts": away_field_goal_attempts,
             "away_field_goal_makes": away_field_goals_made,
             "away_field_goal_percentage": away_field_goal_percentage,
             "home_longest_field_goal": home_longest_field_goal,
             "away_longest_field_goal": away_longest_field_goal,
             "home_longest_touchdown": home_longest_touchdown,
             "away_longest_touchdown": away_longest_touchdown,
             "home_passing_attempts": home_passing_attempts,
             "home_passing_completions": home_passing_completions,
             "home_passing_percentage": home_passing_percentage,
             "away_passing_attempts": away_passing_attempts,
             "away_passing_completions": away_passing_completions,
             "away_passing_percentage": away_passing_percentage,
             "home_rushing_attempts": home_rushing_attempts,
             "home_rushing_successes": home_rushing_successes,
             "home_rushing_percentage": home_rushing_percentage,
             "away_rushing_attempts": away_rushing_attempts,
             "away_rushing_successes": away_rushing_successes,
             "away_rushing_percentage": away_rushing_percentage,
             "home_third_down_attempts": home_third_down_attempts,
             "home_third_down_successes": home_third_down_successes,
             "home_third_down_percentage": home_third_down_percentage,
             "away_third_down_attempts": away_third_down_attempts,
             "away_third_down_successes": away_third_down_successes,
             "away_third_down_percentage": away_third_down_percentage,
             "home_fourth_down_attempts": home_fourth_down_attempts,
             "home_fourth_down_successes": home_fourth_down_successes,
             "home_fourth_down_percentage": home_fourth_down_percentage,
             "away_fourth_down_attempts": away_fourth_down_attempts,
             "away_fourth_down_successes": away_fourth_down_successes,
             "away_fourth_down_percentage": away_fourth_down_percentage,
             "home_two_point_attempts": home_two_point_attempts,
             "home_two_point_successes": home_two_point_successes,
             "home_two_point_percentage": home_two_point_percentage,
             "away_two_point_attempts": away_two_point_attempts,
             "away_two_point_successes": away_two_point_successes,
             "away_two_point_percentage": away_two_point_percentage,
             "home_onside_kick_attempts": home_onside_kick_attempts,
             "home_onside_kick_successes": home_onside_kick_successes,
             "home_onside_kick_percentage": home_onside_kick_percentage,
             "away_onside_kick_attempts": away_onside_kick_attempts,
             "away_onside_kick_successes": away_onside_kick_successes,
             "away_onside_kick_percentage": away_onside_kick_percentage,
             "home_offensive_plays": home_offensive_plays,
             "home_defensive_plays": home_defensive_plays,
             "away_offensive_plays": away_offensive_plays,
             "away_defensive_plays": away_defensive_plays,
             "home_turnovers": home_turnovers,
             "home_fumbles": home_fumbles,
             "home_interceptions": home_interceptions,
             "away_turnovers": away_turnovers,
             "away_fumbles": away_fumbles,
             "away_interceptions": away_interceptions,
             "home_defensive_touchdowns": home_defensive_touchdowns,
             "home_scoop_and_scores": home_scoop_and_scores,
             "home_pick_sixes": home_pick_sixes,
             "home_kickoff_defensive_touchdowns": home_kickoff_defensive_touchdowns,
             "away_defensive_touchdowns": away_defensive_touchdowns,
             "away_scoop_and_scores": away_scoop_and_scores,
             "away_pick_sixes": away_pick_sixes,
             "away_kickoff_defensive_touchdowns": away_kickoff_defensive_touchdowns,
             "win_probability": plays[-1]["win_probability"]}

    return stats
