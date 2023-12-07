from Database.database_configuration import parse_yaml
import psycopg2
from Constants.queries import CREATE_ISS_WAREHOUSE_TABLE
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    # connect to the database
    def connect(self):
        """connects to iss database"""
        try:
            parameters = parse_yaml()
            self.connection = psycopg2.connect(**parameters)
            self.cursor = self.connection.cursor()
        except psycopg2.DatabaseError as error:
            logger.error(f"error while connecting: {error}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
        if self.cursor:
            self.cursor.close()

