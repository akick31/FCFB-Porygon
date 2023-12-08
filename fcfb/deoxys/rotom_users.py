import requests

ROTOM_USERS_PATH = "rotom_users/"


async def add_user(config_data, discord_id, discord_username, reddit_username):
    """
    Make API call to add a user to the database

    :param config_data:
    :param discord_id:
    :param discord_username:
    :param reddit_username:
    :return:
    """

    try:
        payload = f"create/{discord_id}/{discord_username}/{reddit_username}"
        endpoint = config_data['api']['url'] + ROTOM_USERS_PATH + payload
        response = requests.post(endpoint)

        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCCESS: Added user to the database")
            return response.json()
        else:
            raise Exception(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")


async def get_user_by_reddit_username(config_data, reddit_username):
    """
    Make API call to get a user from the database

    :return:
    """

    try:
        payload = f"reddit_username/{reddit_username}"
        endpoint = config_data['api']['url'] + ROTOM_USERS_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCCESS: Retrieved user from the database using their reddit username")
            return response.json()
        else:
            return
    except Exception as e:
        raise Exception(f"{e}")


async def delete_user(config_data, discord_id):
    """
    Make API call to delete a user from the database

    :param config_data:
    :param discord_id:
    :return:
    """

    try:
        payload = f"{discord_id}"
        endpoint = config_data['api']['url'] + ROTOM_USERS_PATH + payload
        response = requests.delete(endpoint)

        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCCESS: Deleted user from the database")
            return True
        else:
            raise Exception(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")
