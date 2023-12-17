import json
from datetime import datetime, timezone
from fcfb.api.deoxys.games import save_game, get_game, update_game, get_unfinished_games
from fcfb.api.deoxys.teams import update_team_stats
from fcfb.discord.discord_interactions import get_channel_by_id, create_message
from fcfb.stats.elo import calc_game_elo
from fcfb.stats.team_stats import calculate_team_stats
from fcfb.stats.vegas import calculate_spread
from fcfb.stats.win_probability import calculate_win_probability
from fcfb.utils.exception_handling import async_exception_handler
from fcfb.utils.setup import setup
from fcfb.reddit.wiki.crawl_game_wiki import get_ongoing_games
from fcfb.reddit.game_threads.game_data import extract_team_info, extract_game_state_info, extract_team_stats, \
    extract_waiting_on_and_gist, extract_end_of_game_info, extract_game_date_info
from fcfb.gist.play_gist import extract_plays_from_gist
from fcfb.api.deoxys.game_plays import save_play
from fcfb.stats.game_stats import calculate_game_stats

config_data, r, logger = setup()
subreddit = r.subreddit(config_data['reddit']['subreddit'])


@async_exception_handler()
async def ongoing_game_crawler(client):
    """
    Crawl the game wiki and extract the ongoing games

    :param client:
    :return:
    """

    try:
        game_list = await get_ongoing_games()
        for game in game_list:
            await extract_game_info_and_save(client, game)

        # Iterate through the list of games in the db that aren't finished and update them
        game_list = await get_unfinished_games()
        for game in game_list:
            game = {
                "away": game["awayTeam"],
                "home": game["homeTeam"],
                "quarter": game["quarter"],
                "playclock": game["gameTimer"],
                "thread": game["thread"],
                "home score": game["homeScore"],
                "away score": game["awayScore"],
                "clock": game["clock"],
                "timestamp": game["threadTimestamp"]
            }
            await extract_game_info_and_save(client, game)

        # TODO: Test coordinators
    except Exception as e:
        raise Exception(f"{e}")


async def extract_game_info_and_save(client, game):
    """
    Extract game information from the game thread and save it to the database

    :param client:
    :param game:
    :return:
    """

    try:
        # Fix team names
        if '&amp;' in game['home']:
            game['home'] = game['home'].replace('&amp;', '&')
        if '&amp;' in game['away']:
            game['away'] = game['away'].replace('&amp;', '&')

        game_thread_url = game["thread"]
        home_team = game["home"]
        away_team = game["away"]

        # Gather info from the game thread
        # Get the game thread
        game_thread = r.submission(url=game_thread_url)
        game_thread_text = game_thread.selftext

        # Set the timestamp
        timestamp = game_thread.created_utc
        utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
        # Format the datetime object as a string in mm/dd/yyyy format
        game["timestamp"] = utc_datetime.strftime("%m/%d/%Y")

        # Get the game ID
        game_id = game_thread.id

        # Extract the playbook and coaches
        team_info = extract_team_info(game_thread_text)

        # Extract the team stats
        team_stats = extract_team_stats(game_thread_text)

        # Extract the game state information
        game_state_info = extract_game_state_info(game_thread_text)

        # Extract if game is in OT or is done
        end_of_game_info = extract_end_of_game_info(game_thread_text)

        # Extract the season and week
        game_date_info = await extract_game_date_info(game["timestamp"])

        # Extract the waiting on and gist
        waiting_on_and_gist = extract_waiting_on_and_gist(game_thread_text)

        if team_info is None or team_stats is None or game_state_info is None or waiting_on_and_gist is None:
            message = f"Failed to extract information from {game_thread}, skipping to the next game"
            logger.info(message)
            channel = await get_channel_by_id(client, config_data["discord"]["log_channel_id"])
            await create_message(channel, f"INFO: {message}")
            return

        # Gather plays from the gist
        gist_url = waiting_on_and_gist["gist_link"]
        plays = await extract_plays_from_gist(gist_url, home_team, away_team, game_id)

        # Check if the game is up to date, if so, just skip it to avoid extra API calls
        game_from_db = await get_game(game_id)
        if game_from_db is not None and int(game_from_db["numPlays"]) == len(plays):
            message = f"Game {game_id} is up to date, skipping"
            logger.info(message)
            return

        # Calcualate the win probability for each play
        plays = await calculate_win_probability(team_info, plays, game_date_info)

        # Calculate the game stats
        stats = calculate_game_stats(plays, team_stats, game["playclock"])
        game.pop("playclock", None) # No need to have two playclocks

        # Calculate the spread
        spread = await calculate_spread(team_info, game_date_info["season"], game_date_info["week"])

        # Put together the game data as a json
        game['game_id'] = game_id
        game_json, game_str = gather_game_data(game, team_info, game_state_info, end_of_game_info, game_date_info,
                                     waiting_on_and_gist, stats, spread)

        # Save the plays in the database
        for play in plays:
            await save_play(play)

        # Save the game in the database
        game_exists = await get_game(game_id)
        if game_exists is not None:
            await update_game(game_id, game_str)
        else:
            await save_game(game_id, game_str)

        if game_json["is_final"]:
            await finalize_game(game_json)

        # TODO: Generate plots and scorebugs

    except Exception as e:
        raise Exception(f"{e}")


def gather_game_data(game, team_info, game_state_info, end_of_game_info, game_date_info, waiting_on_and_gist, stats,
                     spread):
    """
    Put together the game data

    :param game:
    :param team_info:
    :param game_state_info:
    :param end_of_game_info:
    :param game_date_info:
    :param waiting_on_and_gist:
    :param stats:
    :param spread:

    :return:
    """

    # Drop the old home/away keys
    game.pop('home', None)
    game.pop('away', None)
    game.update(team_info)

    # Parse down and distance into separate fields
    game.update(game_state_info)
    game['down'] = game['down_and_distance'].split('&')[0].strip()
    if game['down'] == '4th':
        game['down'] = 4
    elif game['down'] == '3rd':
        game['down'] = 3
    elif game['down'] == '2nd':
        game['down'] = 2
    elif game['down'] == '1st':
        game['down'] = 1
    game['yards_to_go'] = int(game['down_and_distance'].split('&')[1].strip())
    game.pop('down_and_distance', None)

    game.update(end_of_game_info)
    game.update(game_date_info)
    game.update(waiting_on_and_gist)
    game.update(stats)
    game.update(spread)

    if game["is_final"]:
        game["clock"] = "0:00"

    game["home_score"] = game["home score"]
    game["away_score"] = game["away score"]
    game["thread_timestamp"] = game["timestamp"]
    game.pop("timestamp", None)
    game.pop("home score", None)
    game.pop("away score", None)

    return game, json.dumps(game)


async def finalize_game(game_json):
    """
    Finalize the game

    :param game_json:
    :return:
    """

    await calc_game_elo(game_json)
    home_team_stats, away_team_stats = await calculate_team_stats(game_json)
    await update_team_stats(game_json["home_team"], home_team_stats)
    await update_team_stats(game_json["away_team"], away_team_stats)