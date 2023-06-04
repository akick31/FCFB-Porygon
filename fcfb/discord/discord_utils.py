import discord
import sys

import pathlib

sys.path.append("..")

from fcfb.utils.vegas_odds import get_vegas_odds


async def create_ongoing_game_message(message, game_info):
    """
    Create the ongoing game message to be posted to Discord

    :param message:
    :param game_info:
    :return:
    """

    home_team = game_info[1]
    away_team = game_info[2]

    vegas_odds = get_vegas_odds(home_team, away_team)[0]

    cur_possession = game_info[11]
    cur_win_probability = game_info[29]

    if cur_possession == game_info[1]:
        home_win_probability = 100 - cur_win_probability
    else:
        home_win_probability = cur_win_probability

    cur_yard_line = game_info[14]
    game_url = game_info[26]

    odds = round(vegas_odds * 2) / 2
    if odds == 0:
        odds_msg = "Push"
    elif odds > 0:
        odds_msg = home_team + " +" + str(odds)
    else:
        odds_msg = home_team + " " + str(odds)

    win_percentage_msg = "Each team has a 50% chance to win\n"
    if int(home_win_probability) >= 50:
        win_percentage_msg = home_team + " has a " + str(int(home_win_probability)) + "% chance to win\n"
    elif int(home_win_probability) < 50:
        win_percentage_msg = away_team + " has a " + str(100 - int(home_win_probability)) + "% chance to win\n"

    embed = discord.Embed(title="**Game Information**", color=0x005EB8)
    embed.add_field(name="**Watch**", value="[Game Thread](" + game_url + ")", inline=False)
    embed.add_field(name="**Spread**", value=odds_msg, inline=False)
    embed.add_field(name="**Win Probability**", value=win_percentage_msg, inline=False)

    scorebug = game_info[25]

    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    print(proj_dir)

    with open(scorebug, 'rb') as fp:
        file = discord.File(fp, 'posted_scorebug.png')
        embed.set_image(url="attachment://posted_scorebug.png")

    embed.add_field(name="**Ball Location**", value=cur_yard_line, inline=False)
    await message.channel.send(embed=embed, file=file)

    print("Comment posted for " + home_team + " vs " + away_team + "\n\n")