# import sys
#
# from fcfb.discord.discord_interactions import create_ongoing_game_message, create_plot_message
#
# sys.path.append("..")
#
# from fcfb.database.communicate_with_database import retrieve_current_season_from_table, retrieve_row_from_table
#
#
# async def parse_commands(config_data, prefix, message, logger):
#     """
#     Handle commands from Discord users
#
#     :param config_data:
#     :param prefix:
#     :param message:
#     :param logger:
#     :return:
#     """
#
#     message_content = message.content.lower()
#
#     # Handle ongoing games score command
#     if message_content.startswith(prefix + 'score'):
#         team = message_content.split('score')[1].strip()
#         game_info = await find_ongoing_game(config_data, team, message, logger)
#         await create_ongoing_game_message(message, game_info)
#
#     elif message_content.startswith(prefix + 'plot'):
#         team = message_content.split('plot')[1].strip()
#         game_info = await find_ongoing_game(config_data, team, message, logger)
#         await create_plot_message(message, game_info)
#
#
# async def find_ongoing_game(config_data, team, message, logger):
#     """
#     Find ongoing game for a team
#
#     :param config_data:
#     :param team:
#     :param message:
#     :param logger:
#     :return:
#     """
#
#     game_info = await retrieve_row_from_table(config_data, "ongoing_games", "home_team", team, logger)
#     if not game_info:
#         game_info = await retrieve_row_from_table(config_data, "ongoing_games", "away_team", team, logger)
#         if not game_info:
#             await message.channel.send("**ALERT: No ongoing game found for " + team + "**")
#             return
#
#     game_info = game_info[0]
#     return game_info
