import psycopg2

from Database.DBManager import DatabaseConnector
from Constants.queries import CREATE_ISS_NORMALIZED_TABLE, INSERT_INTO_NORMALIZED_TABLE, CREATE_ECLIPSED_PARTITION, CREATE_DAYLIGHT_PARTITION
from Constants.variables import DISTANCE_UNIT
from Database.warehouse_data_formatting import WarehouseDataFormatter
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class WarehouseToIssTable:
    def __init__(self):
        self.df = WarehouseDataFormatter().wrapper_function()
        self.connector = DatabaseConnector()

    def create_table_if_not_exists(self):
        """Create 'iss_normalized' table if it does not exist."""
        try:
            self.connector.connect()
            self.connector.cursor.execute(CREATE_ISS_NORMALIZED_TABLE)
            self.connector.cursor.execute(CREATE_DAYLIGHT_PARTITION)
            self.connector.cursor.execute(CREATE_ECLIPSED_PARTITION)

            self.connector.connection.commit()  # Commit the creation of 'iss_normalized'
            logger.info('Table "iss_normalized" created successfully')
        except Exception as exception:
            logger.error(f'Error creating table "iss_normalized": {exception}')

    def insert_into_normalized_table(self):
        """cleaned up data is presented as pandas Series object
        method inserts it in iss_normalized"""
        try:
            self.connector.connect()

            values = (
                self.df['latitude'],
                self.df['longitude'],
                self.df['visibility'],
                self.df['date'],
                self.df['current_location'],
                self.df['distance_travelled'],
                DISTANCE_UNIT
            )
            self.connector.cursor.execute(INSERT_INTO_NORMALIZED_TABLE, values)
            self.connector.connection.commit()
            print("inserted in table iss_normalized")
        except psycopg2.errors.UndefinedTable as e:

            # if the table does not exist. gives us error, create the table
            self.connector.connect()
            self.connector.cursor.execute(CREATE_ISS_NORMALIZED_TABLE)
            self.connector.cursor.execute(CREATE_DAYLIGHT_PARTITION)
            self.connector.cursor.execute(CREATE_ECLIPSED_PARTITION)

            self.connector.connection.commit()  # Commit the creation of 'iss_normalized'
            logger.info('Table "iss_normalized" created successfully')

            # call the function again
            self.insert_into_normalized_table()
        except Exception as exception:
            logger.error(f'Error creating table "iss_normalized": {exception}')
