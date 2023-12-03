import pandas as pd
from Constants.queries import INSERT_ISS_INFO_WAREHOUSE, SELECT_DATA_IN_RANGE_QUERY
from Logger.iss_logger import setup_logging
import logging
from datetime import datetime
import json

setup_logging()
logger = logging.getLogger(__name__)


class ISSWarehouse:
    def __init__(self, dataframe=None):
        self.dataframe = dataframe
        self.last_timestamp_retrieved = None # will use this to select parts of ra json file

    def load_data_from_json(self, path_to_json: str) -> None:
        """loads json data as pandas dataframe"""
        with open(path_to_json, 'r') as json_file:
            raw_data = json.load(json_file)

        self.dataframe = pd.DataFrame(raw_data)

    def select_data_from_json(self, path_to_json: str) -> None:
        """select specific part of data from json file
        those that have not been inserted to database yet"""
        try:
            self.load_data_from_json(path_to_json)
            self.convert_timestamp_to_datetime()
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # update timestamp in both cases
            # Load data from JSON file
            if self.last_timestamp_retrieved is None:
                self.last_timestamp_retrieved = current_timestamp # it timestamp is None, means we need all the data
            else:
                self.dataframe = self.dataframe[
                    (self.dataframe["timestamp"] > self.last_timestamp_retrieved) &
                    (self.dataframe["timestamp"] < current_timestamp)
                    ]
                self.last_timestamp_retrieved = current_timestamp # if not None, select data between timestampt and current time

        except Exception as exception:
            logger.error(f'Error selecting and updating timestamp: {exception}')


    def convert_timestamp_to_datetime(self, column_name='timestamp') -> pd.DataFrame:
        """Convert timestamp to datetime in the specified column and add 4 hours"""
        try:
            if column_name in self.dataframe.columns:
                # some of the rows have invalid timestamp, taht is out of range
                invalid_mask = (self.dataframe['timestamp'] <= 0) | (
                        self.dataframe['timestamp'] > pd.Timestamp.now().timestamp())
                self.dataframe = self.dataframe.loc[~invalid_mask] # I drop those rows

                # convert to datetime
                self.dataframe['timestamp'] = pd.to_datetime(self.dataframe['timestamp'], unit='s', utc=True)

                # add 4 hours for time zone difference
                self.dataframe['timestamp'] = self.dataframe['timestamp'] + pd.Timedelta(hours=4)

                # Format the timestamp as a string
                self.dataframe['timestamp'] = self.dataframe['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

                return self.dataframe
            else:
                raise ValueError(f"Column '{column_name}' not found in the dataframe.")
        except Exception as exception:
            logger.error(f'Error converting timestamp to datetime: {exception}')


    def change_kilometer(self) -> None:
        """simply change kilometers to km"""
        self.dataframe["units"] = 'km'

    def insert_to_warehouse(self, db_connector) -> None:
        """insert DataFrame into the ISS warehouse table"""
        try:
            db_connector.connect()
            # unpack values to insert
            records = [{k: v for k, v in record.items() if k not in ('name', 'id')} for record in self.dataframe.to_dict(orient='records')]
            db_connector.cursor.executemany(INSERT_ISS_INFO_WAREHOUSE, [tuple(record.values()) for record in records])
            db_connector.connection.commit()

            print(" all the rows inserted in iss_24455_warehouse")
        except Exception as exception:
            logger.error(f'exception while inserting data into warehouse: {exception}')

    def select_data_in_range(self, five_minutes_ago: datetime, current_timestamp: datetime, db_connector) -> tuple[pd.DataFrame, pd.DataFrame]:
        """two arguments are timestamp when the method is called and timestamp 5 min before
        based on that method selects all the data in that range"""
        try:
            db_connector.connect()

            # double check timestamp format
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
