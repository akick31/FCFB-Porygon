import discord
import sys

sys.path.append("..")

from fcfb.discord.discord_commands import handle_commands

def run_porygon_bot(config_data, logger):
    """
    Run Porygon bot

    :param config_data:
    :param logger:
    :return:
    """

    token = config_data['discord_token']
    prefix = config_data['prefix']

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        if message.content.startswith(prefix):
            await handle_commands(config_data, prefix, message, logger)

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)