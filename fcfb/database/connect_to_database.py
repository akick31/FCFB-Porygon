import mariadb


async def connect_to_db(config_data):
    """
    Connect to the database

    :return:
    """

    # Connect to MariaDB Platform
    try:
        db = mariadb.connect(
            user=config_data['db_user'],
            password=config_data['db_password'],
            host=config_data['db_host'],
            port=int(config_data['db_port']),
            database=config_data['db_name'],
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

    return db
