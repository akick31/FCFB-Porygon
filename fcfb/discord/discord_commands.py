import sys

from fcfb.discord.discord_utils import create_ongoing_game_message

sys.path.append("..")

from fcfb.database.communicate_with_database import retrieve_current_season_from_table, retrieve_row_from_table


async def handle_commands(config_data, prefix, message, logger):
    """
    Handle commands from Discord users

    :param config_data:
    :param prefix:
    :param message:
    :param logger:
    :return:
    """

    message_content = message.content.lower()

    # Handle ongoing games
    if message_content.startswith(prefix + 'score'):
        team = message_content.split('score')[1].strip()
        game_info = await retrieve_row_from_table(config_data, "ongoing_games", "home_team", team, logger)
        if not game_info:
            game_info = await retrieve_row_from_table(config_data, "ongoing_games", "away_team", team, logger)
            if not game_info:
                await message.channel.send("**ALERT: No ongoing game found for " + team + "**")
                return

        game_info = game_info[0]
        await create_ongoing_game_message(message, game_info)
