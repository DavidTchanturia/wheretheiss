import pandas as pd
from Constants.queries import INSERT_ISS_INFO_WAREHOUSE, SELECT_ALL_FROM_ISS_WAREHOUSE, SELECT_DATA_IN_RANGE_QUERY
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class ISSWarehouse:
    def __init__(self, dataframe=None):
        self.dataframe = dataframe

    def convert_timestamp_to_datetime(self, column_name='timestamp'):
        """Convert timestamp to datetime in the specified column"""
        try:
            if column_name in self.dataframe.columns:
                self.dataframe['timestamp'] = pd.to_datetime(self.dataframe['timestamp'], unit='s', utc=True)
                self.dataframe['timestamp'] = self.dataframe['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

                # Convert daynum to decimal
                if 'daynum' in self.dataframe.columns:
                    self.dataframe['daynum'] = self.dataframe['daynum'].astype(float)

                logger.info(f'Timestamp converted to datetime in column "{column_name}" successfully')
                return self.dataframe
            else:
                raise ValueError(f"Column '{column_name}' not found in the dataframe.")
        except Exception as exception:
            logger.error(f'Error converting timestamp to datetime: {exception}')

    def change_kilometer(self):
        """simply change kilometers to km"""
        self.dataframe["units"] = 'km'

    def insert_to_warehouse(self, db_connector):
        """insert DataFrame into the ISS warehouse table"""
        try:
            db_connector.connect()
            #
            records = [{k: v for k, v in record.items() if k not in ('name', 'id')} for record in self.dataframe.to_dict(orient='records')]
            db_connector.cursor.executemany(INSERT_ISS_INFO_WAREHOUSE, [tuple(record.values()) for record in records])
            db_connector.connection.commit()

            print("Data inserted into warehouse")
        except Exception as exception:
            logger.error(f'exception while inserting data into warehouse: {exception}')

    def select_data_in_range(self, five_minutes_ago, current_timestamp, db_connector):
        """two arguments are timestamp when the method is called and timestamp 5 min before
        based on that method selects all the data in that range"""
        try:
            db_connector.connect()

            # Ensure start_timestamp and end_timestamp are in datetime format
            start_timestamp = pd.to_datetime(five_minutes_ago, format='%Y-%m-%d %H:%M:%S')
            end_timestamp = pd.to_datetime(current_timestamp, format='%Y-%m-%d %H:%M:%S')

            # Select data within the specified date range
            query = SELECT_DATA_IN_RANGE_QUERY.format(five_minutes_ago=start_timestamp, current_timestamp=end_timestamp)
            db_connector.cursor.execute(query)
            result = db_connector.cursor.fetchall()
            column_names = [desc[0] for desc in db_connector.cursor.description]

            df = pd.DataFrame(result, columns=column_names)

            # get the max and min timestamp in that range to calculate distance difference
            if not df.empty:
                starting_point = df.loc[df['date'].idxmin()]
                ending_point = df.loc[df['date'].idxmax()]

                return starting_point, ending_point
            else:
                return pd.DataFrame(), pd.DataFrame()

        finally:
            db_connector.close_connection()
