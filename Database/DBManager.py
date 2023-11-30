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
        """connects to iss datbase"""
        try:
            parameters = parse_yaml()
            self.connection = psycopg2.connect(**parameters)
            self.cursor = self.connection.cursor()
        except psycopg2.DatabaseError as error:
            logger.error(f"error while connecting: {error}")
        except Exception as exception:
            logger.error(f"exception occured while parsing yaml folder: {exception}")

    def close_connection(self):
        try:
            if self.connection:
                self.connection.close()
            if self.cursor:
                self.cursor.close()
        except Exception as exception:
            logger.error(f"{exception} encountered while closing connection")


class ISSDataWarehouseManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_table(self):
        """create movies table if it does not exist"""
        try:
            self.db_connector.connect()
            self.db_connector.cursor.execute(CREATE_ISS_WAREHOUSE_TABLE)
            self.db_connector.connection.commit()
        except Exception as exception:
            logger.error(f"An unexpected error occurred: {exception}")