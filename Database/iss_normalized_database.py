from Database.DBManager import DatabaseConnector
from Constants.queries import CREATE_ISS_NORMALIZED_TABLE, INSERT_INTO_NORMALIZED_TABLE
from Database.warehouse_data_formatting import just_for_test

class ISSNormalizedDatabase:
    def __init__(self, df=None):
        self.df = just_for_test()
        self.connector = DatabaseConnector()

    def create_table_if_not_exists(self):
        """create movies table if it does not exist"""
        try:
            self.connector.connect()
            self.connector.cursor.execute(CREATE_ISS_NORMALIZED_TABLE)
            self.connector.connection.commit()
            print("table created")
        finally:
            self.connector.close_connection()

    def insert_into_normalized_table(self):
        try:
            self.connector.connect()

            values = (
                self.df['latitude'],
                self.df['longitude'],
                self.df['visibility'],
                self.df['date'],
                self.df['current_location'],
                self.df['distance_travelled'],
                "km"
            )
            self.connector.cursor.execute(INSERT_INTO_NORMALIZED_TABLE, values)
            self.connector.connection.commit()
            print("Data inserted into the table")
        finally:
            self.connector.close_connection()