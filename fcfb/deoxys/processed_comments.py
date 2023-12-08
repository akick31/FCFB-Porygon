import requests

PROCESSED_COMMENTS_PATH = "processed_comments/"


async def get_processed_comment(config_data, comment_id):
    """
    Make API call to get processed comment from the database

    :param config_data:
    :param comment_id:
    :return:
    """

    try:
        payload = f"comment_id/{comment_id}"
        endpoint = config_data['api']['url'] + PROCESSED_COMMENTS_PATH + payload
        response = requests.get(endpoint)

        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCCESS: Retrieved processed comment from the the database")
            return response.json()
        else:
            return

    except Exception as e:
        raise Exception(f"{e}")


async def add_processed_comment(config_data, comment_id, submission_id):
    """
    Make API call to add a processed comment to the database

    :param config_data:
    :param comment_id:
    :param submission_id:
    :return:
    """

    try:
        payload = f"create/{comment_id}/{submission_id}"
        endpoint = config_data['api']['url'] + PROCESSED_COMMENTS_PATH + payload
        response = requests.post(endpoint)

        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCCESS: Added processed comment to the database")
            return response.json()
        else:
            raise Exception(f"HTTP {response.status_code} response {response.text}")

    except Exception as e:
        raise Exception(f"{e}")