from Database.DBManager import DatabaseConnector
from Database.iss_wearhouse import ISSWarehouse
from GetData.get_iss_location import ISSLocation

class ISSNormalizedDatabase:
    def __init__(self) -> None:
        self.connector = DatabaseConnector()
        self.iss_warehouse = ISSWarehouse()
        self.normalized_dataframe = None

    def retrieve_data(self):
        try:
            # Connect to the database
            self.connector.connect()

            # Call the select_all_from_warehouse method from ISSWarehouse
            data = self.iss_warehouse.select_all_from_warehouse(self.connector)
            self.normalized_dataframe = data
            return self.normalized_dataframe
        finally:
            # Close the database connection
            self.connector.close_connection()

    def remove_unnecessary_data(self):
        self.normalized_dataframe.drop(["id", "altitude", "velocity", "footprint", "daynum",
                                        "solar_lat", "solar_lon"], axis='columns', inplace=True)

    def find_iss_location(self):
        if self.normalized_dataframe is not None:
            # Pass DataFrame columns to get_location
            locations = ISSLocation().get_location(
                self.normalized_dataframe["latitude"],
                self.normalized_dataframe["longitude"]
            )

            # Add the 'location' column to the DataFrame
            self.normalized_dataframe["location"] = locations


# Create an instance of ISSNormalizedDatabase
obj = ISSNormalizedDatabase()

obj.retrieve_data()
obj.remove_unnecessary_data()
obj.find_iss_location()
print(obj.normalized_dataframe)

