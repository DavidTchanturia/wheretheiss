import pandas as pd
from Constants.queries import INSERT_ISS_INFO_WAREHOUSE

class ISSWarehouse:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_timestamp_to_datetime(self, column_name='timestamp'):
        """Convert timestamp to datetime in the specified column"""
        if column_name in self.dataframe.columns:
            self.dataframe['timestamp'] = pd.to_datetime(self.dataframe['timestamp'], unit='s', utc=True)
            self.dataframe['timestamp'] = self.dataframe['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Convert daynum to decimal
            if 'daynum' in self.dataframe.columns:
                self.dataframe['daynum'] = self.dataframe['daynum'].astype(float)

            return self.dataframe
        else:
            raise ValueError(f"Column '{column_name}' not found in the dataframe.")

    def change_kilometer(self):
        self.dataframe["units"] = 'km'

    def insert_to_warehouse(self, db_connector):
        """Insert DataFrame into the ISS warehouse table"""
        try:
            db_connector.connect()
            # Insert DataFrame into the database
            records = [{k: v for k, v in record.items() if k not in ('name', 'id')} for record in self.dataframe.to_dict(orient='records')]
            db_connector.cursor.executemany(INSERT_ISS_INFO_WAREHOUSE, [tuple(record.values()) for record in records])
            db_connector.connection.commit()

            print("Data inserted into warehouse")
        finally:
            db_connector.close_connection()