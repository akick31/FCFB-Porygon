import json
from fcfb.api.deoxys.games import save_game
from fcfb.discord.discord_interactions import get_channel_by_id, create_message
from fcfb.utils.exception_handling import async_exception_handler
from fcfb.utils.setup import setup
from fcfb.reddit.wiki.crawl_game_wiki import get_ongoing_games
from fcfb.reddit.game_threads.game_data import extract_team_info, extract_game_state_info, extract_team_stats, \
    extract_waiting_on_and_gist
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

        # TODO: Go through the list of games added that are not marked as finished, get the game id, verify that the game isn't over
        # If the game is over, mark it as finished in the database and finish updating the gist

        # TODO: When the game is over, update the team stats
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
        game_thread_url = game["thread"]
        home_team = game["home"]
        away_team = game["away"]

        # Gather info from the game thread
        # Get the game thread
        game_thread = r.submission(url=game_thread_url)
        game_thread_text = game_thread.selftext

        # Get the game ID
        game_id = game_thread.id

        # Extract the playbook and coaches
        team_info = extract_team_info(game_thread_text)

        # Extract the team stats
        team_stats = extract_team_stats(game_thread_text)

        # Extract the game state information
        game_state_info = extract_game_state_info(game_thread_text)

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

        # Calculate the game stats
        stats = calculate_game_stats(plays, team_stats, game["playclock"])

        # Put together the game data as a json
        game['game_id'] = game_id
        game_json = gather_game_data(game, team_info, game_state_info, waiting_on_and_gist, stats)

        await save_game(game_json)

        # Save the plays in the database
        for play in plays:
            await save_play(play)

        # Save the game in the database
        #if game_exists_in_deoxys(game_id):
        #    update_game(game, playbook_and_coaches, team_stats, game_state_info, waiting_on_and_gist, stats)
        #else:

    except Exception as e:
        raise Exception(f"{e}")


def gather_game_data(game, team_info, game_state_info, waiting_on_and_gist, stats):
    """
    Put together the game data

    :return:
    """

    # Drop the old home/away keys
    game.pop('home', None)
    game.pop('away', None)
    game.update(team_info)

    # Parse down and distance into separate fields
    game.update(game_state_info)
    game['down'] = game['down_and_distance'].split(' ')[0]
    game['yards_to_go'] = game['down_and_distance'].split(' ')[1]
    game.pop('down_and_distance', None)

    game.update(waiting_on_and_gist)
    game.update(stats)

    return json.dumps(game)