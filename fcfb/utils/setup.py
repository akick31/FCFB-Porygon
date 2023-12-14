import logging
import sys
import json
import pathlib
import praw


def setup():
    """
    Setup the application
    :return:
    """

    # Setup logging
    logger = logging_setup()

    # Setup config
    config_data = config_setup()

    # Setup reddit
    reddit = reddit_setup(config_data)

    return config_data, reddit, logger


def reddit_setup(config_data):
    """
    Login to reddit
    :param config_data:
    :return:
    """

    r = praw.Reddit(user_agent=config_data['reddit']['user_agent'],
                    client_id=config_data['reddit']['client_id'],
                    client_secret=config_data['reddit']['client_secret'],
                    username=config_data['reddit']['username'],
                    password=config_data['reddit']['password'],
                    subreddit=config_data['reddit']['subreddit'],
                    check_for_async=False)
    return r


def config_setup():
    """
    Return config data as a json
    :return:
    """

    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    return config_data

def logging_setup():
    """
    Setup logging for the application
    :return:
    """

    # Suppress discord gateway warnings
    logging.getLogger("discord.gateway").setLevel(logging.ERROR)

    # Create logger
    logger = logging.getLogger('fcfb_porygon')
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)

    # Add stream handler to logger
    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    return logger



