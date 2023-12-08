import discord
import sys

from fcfb.utils.exception_handling import async_exception_handler, DiscordAPIError

sys.path.append("..")


# async def create_ongoing_game_message(message, game_info):
#     """
#     Create the ongoing game message to be posted to Discord
#
#     :param message:
#     :param game_info:
#     :return:
#     """
#
#     home_team = game_info[1]
#     away_team = game_info[2]
#
#     vegas_odds = get_vegas_odds(home_team, away_team)[0]
#
#     cur_possession = game_info[11]
#     cur_win_probability = game_info[29]
#
#     if cur_possession == game_info[1]:
#         home_win_probability = 100 - cur_win_probability
#     else:
#         home_win_probability = cur_win_probability
#
#     cur_yard_line = game_info[14]
#     game_url = game_info[26]
#
#     odds = round(vegas_odds * 2) / 2
#     if odds == 0:
#         odds_msg = "Push"
#     elif odds > 0:
#         odds_msg = home_team + " +" + str(odds)
#     else:
#         odds_msg = home_team + " " + str(odds)
#
#     win_percentage_msg = "Each team has a 50% chance to win\n"
#     if int(home_win_probability) >= 50:
#         win_percentage_msg = home_team + " has a " + str(int(home_win_probability)) + "% chance to win\n"
#     elif int(home_win_probability) < 50:
#         win_percentage_msg = away_team + " has a " + str(100 - int(home_win_probability)) + "% chance to win\n"
#
#     embed = discord.Embed(title="**Game Information**", color=0x005EB8)
#     embed.add_field(name="**Watch**", value="[Game Thread](" + game_url + ")", inline=False)
#     embed.add_field(name="**Spread**", value=odds_msg, inline=False)
#     embed.add_field(name="**Win Probability**", value=win_percentage_msg, inline=False)
#
#     scorebug = game_info[25]
#
#     scorebug = "/project/../fcfb/graphics/scorebugs/" + scorebug.split("fcfb_scorebugs/")[1]
#
#     with open(scorebug, 'rb') as fp:
#         file = discord.File(fp, 'posted_scorebug.png')
#         embed.set_image(url="attachment://posted_scorebug.png")
#
#     embed.add_field(name="**Ball Location**", value=cur_yard_line, inline=False)
#     await message.channel.send(embed=embed, file=file)
#
#     print("Comment posted for " + home_team + " vs " + away_team + "\n\n")
#
#
# async def create_plot_message(message, game_info):
#     """
#     Create the plot message to be posted to Discord
#
#     :param message:
#     :param game_info:
#     :return:
#     """
#
#     home_team = game_info[1]
#     away_team = game_info[2]
#     wp_chart = game_info[33]
#
#     wp_chart = "/project/../fcfb/graphics/win_probability/" + wp_chart.split("fcfb_win_probability/")[1]
#
#     with open(wp_chart, 'rb') as fp:
#         await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
#
#     print("Plot posted for " + home_team + " vs " + away_team + "\n\n")


@async_exception_handler()
async def create_message(channel, message_text, embed=None):
    """
    Create a message

    :param channel:
    :param message_text:
    :param embed:
    :return:
    """

    try:
        await channel.send(message_text, embed=embed)
    except Exception as e:
        raise DiscordAPIError(f"There was an issue sending a message to the channel, {e}")


@async_exception_handler()
async def get_channel_by_id(client, channel_id):
    """
    Get a Discord channel by ID

    :param client: Discord client object
    :param channel_id: ID of the channel to retrieve
    :return: Channel object or None if not found
    """

    try:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            raise DiscordAPIError(f"Channel with ID {channel_id} not found")
        return channel
    except Exception as e:
        raise DiscordAPIError(f"There was an issue getting the channel by its ID, {e}")
