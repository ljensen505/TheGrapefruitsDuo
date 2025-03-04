import os

import mysql.connector
from dotenv import load_dotenv


class DBException(Exception):
    pass


def connect_db() -> mysql.connector.MySQLConnection:
    """
    Connects to the MySQL database using credentials from the .env file.
    Returns a MySQLConnection object which can be used by the database query layer.

    Credential values are validated and an exception is raised if any are missing.
    """
    load_dotenv(override=True)
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")

    if None in [host, user, password, database]:
        raise DBException("Missing database credentials")

    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin="mysql_native_password",
        )  # type: ignore

    except mysql.connector.Error as err:
        raise DBException("Could not connect to database") from err
