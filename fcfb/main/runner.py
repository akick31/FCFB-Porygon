import discord
from discord.ext import tasks
#from fcfb.discord.commands import parse_commands
from fcfb.discord.discord_interactions import create_message, get_channel_by_id
from fcfb.utils.exception_handling import async_exception_handler
from fcfb.utils.setup import setup
from fcfb.reddit.wiki.crawl_game_wiki import crawl

config_data, r, logger = setup()


def run_porygon_bot():
    """
    Run Porygon bot

    :param config_data:
    :param logger:
    :return:
    """

    token = config_data['discord']['token']
    prefix = config_data['discord']['prefix']

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    client = discord.Client(intents=intents)

    @tasks.loop(seconds=10)
    @async_exception_handler()
    async def reddit_crawler():
        try:
            await crawl()
        except Exception as e:
            channel = await get_channel_by_id(client, config_data["error_channel_id"])
            await create_message(channel, f"{e}")
            logger.error(f"{e}")

    # @client.event
    # @async_exception_handler()
    # async def on_message(message):
    #     if message.content.startswith(prefix):
    #         await parse_commands(config_data, prefix, message, logger)

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        reddit_crawler.start()

    client.run(token)
