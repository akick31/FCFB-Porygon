import logging
from fcfb.database.connect_to_database import connect_to_db

async def retrieve_row_from_table(config_data, table_name, where_column, where_value, logger):
    """
    Retrieve a row in a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param where_value:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name +
                       " WHERE UPPER(" + where_column + ") LIKE UPPER('" + where_value + "')")
        row = cursor.fetchall()
        db.close()
        return row
    except Exception as e:
        logger.error("Error retrieving row from database table " + table_name + ": " + str(e))
        db.close()
        return None


async def retrieve_value_from_table(config_data, table_name, where_column, where_value, column, logger):
    """
    Retrieve a value from a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param where_value:
    :param column:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT " + column + " FROM " + table_name +
                       " WHERE " + where_column + "='" + where_value + "'")
        value = cursor.fetchone()
        db.close()
        if value is None:
            return None
        return value[0]
    except Exception as e:
        logger.error("Error retrieving value from database table " + table_name + ": " + str(e))
        db.close()
        return None


async def retrieve_current_season_from_table(config_data, logger):
    """
    Retrieve a current season from a table

    :param config_data:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM seasons " +
                       "ORDER BY season DESC LIMIT 1")
        season = cursor.fetchone()
        db.close()
        return season[0]
    except Exception as e:
        logger.error("Error retrieving season from seasons table: " + str(e))
        db.close()
        return None

async def get_all_rows_in_table(config_data, table_name, logger):
    """
    Return all rows in a table

    :param config_data:
    :param table_name:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        db.close()
        return rows
    except Exception as e:
        logger.error("Error retrieving all rows in database table " + table_name + ": " + str(e))
        db.close()
        return None


async def get_all_values_in_column_from_table(config_data, table_name, column_name, logger):
    """
    Return all values in a column from a table

    :param config_data:
    :param table_name:
    :param column_name:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT " + column_name + " FROM " + table_name)
        values = cursor.fetchall()
        db.close()
        return [value[0] for value in values]
    except Exception as e:
        logger.error("Error retrieving all values in column " + column_name + " from database table " + table_name
                     + ": " + str(e))
        db.close()
        return None


async def get_all_rows_where_value_in_column_from_table(config_data, table_name, column_name, value, logger):
    """
    Return all rows where a value is in a column from a table

    :param config_data:
    :param table_name:
    :param column_name:
    :param value:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()

        if isinstance(value, int) or isinstance(value, float):
            cursor.execute("SELECT * FROM " + table_name + " WHERE " + column_name + "=" + str(value))
        else:
            cursor.execute("SELECT * FROM " + table_name + " WHERE " + column_name + "='" + str(value) + "'")
        rows = cursor.fetchall()
        db.close()
        return rows
    except Exception as e:
        logger.error("Error retrieving all values in column " + column_name + " from database table " + table_name
                     + ": " + str(e))
        db.close()
        return None
