import pandas as pd
import psycopg2
from Constants.queries import INSERT_ISS_INFO_WAREHOUSE, SELECT_DATA_IN_RANGE_QUERY, CREATE_ISS_WAREHOUSE_TABLE
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON
from datetime import datetime


class JsonToWarehouse:
    def __init__(self, dataframe=None):
        self.dataframe = dataframe
        self.last_timestamp_retrieved = None  # will use this to select parts of raw json file

    def create_iss_warehouse_table(self, db_connector):
        db_connector.connect()
        db_connector.cursor.execute(CREATE_ISS_WAREHOUSE_TABLE)
        db_connector.connection.commit()

    def _select_data_from_json(self, path_to_json: str = PATH_TO_RAW_ISS_INFO_JSON) -> None:
        """select specific part of data from json file
        those that have not been inserted to database yet"""

        self.dataframe = pd.read_json(path_to_json)
        self._convert_timestamp_to_datetime()
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # update timestamp in both cases

        # Add 4 hours to current_timestamp
        current_timestamp = (
                    pd.to_datetime(current_timestamp, format='%Y-%m-%d %H:%M:%S') + pd.Timedelta(hours=4)).strftime(
            '%Y-%m-%d %H:%M:%S')

        # Load data from JSON file
        if self.last_timestamp_retrieved is None:
            self.last_timestamp_retrieved = current_timestamp  # its timestamp is None, means we need all the data
        else:
            self.dataframe = self.dataframe[
                (self.dataframe["timestamp"] > self.last_timestamp_retrieved) &
                (self.dataframe["timestamp"] < current_timestamp)
                ]
            self.last_timestamp_retrieved = current_timestamp

    def _convert_timestamp_to_datetime(self, column_name='timestamp') -> pd.DataFrame:
        """Convert timestamp to datetime in the specified column and add 4 hours"""
        if column_name in self.dataframe.columns:
            # convert to datetime
            self.dataframe['timestamp'] = pd.to_datetime(self.dataframe['timestamp'], unit='s', utc=True)

            # add 4 hours for time zone difference
            self.dataframe['timestamp'] = self.dataframe['timestamp'] + pd.Timedelta(hours=4)

            # Format the timestamp as a string
            self.dataframe['timestamp'] = self.dataframe['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

            return self.dataframe
        else:
            raise ValueError(f"Column '{column_name}' not found in the dataframe.")

    def _insert_to_warehouse(self, db_connector) -> None:
        """insert DataFrame into the ISS warehouse table"""
        try:
            db_connector.connect()
            # unpack values to insert
            records = [{k: v for k, v in record.items() if k not in ('name', 'id')} for record in self.dataframe.to_dict(orient='records')]
            db_connector.cursor.executemany(INSERT_ISS_INFO_WAREHOUSE, [tuple(record.values()) for record in records])
            db_connector.connection.commit()

            print(" all the rows inserted in iss_24455_warehouse")
        except psycopg2.errors.UndefinedTable as e:

            self._insert_to_warehouse(db_connector) # call the function again

    @staticmethod
    def select_data_in_range(five_minutes_ago: datetime, current_timestamp: datetime, db_connector) -> tuple[pd.DataFrame, pd.DataFrame]:
        """two arguments are timestamp when the method is called and timestamp 5 min before
        based on that method selects all the data in that range"""
        try:
            db_connector.connect()

            # double check timestamp format
            start_timestamp = pd.to_datetime(five_minutes_ago, format='%Y-%m-%d %H:%M:%S')
            end_timestamp = pd.to_datetime(current_timestamp, format='%Y-%m-%d %H:%M:%S')

            start_timestamp += pd.Timedelta(hours=4)
            end_timestamp += pd.Timedelta(hours=4)

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

    def get_warehouse_data_wrapper(self, db_connector):
        self._select_data_from_json(PATH_TO_RAW_ISS_INFO_JSON)  # selects data that has not been inserted to warehouse
        self.dataframe["units"] = 'km'  # change kilometers -> km
        self._insert_to_warehouse(db_connector)  # insert into iss_24455_warehouse
