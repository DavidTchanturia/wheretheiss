from Database.DBManager import DatabaseConnector
from Database.iss_wearhouse import ISSWarehouse
from GetData.get_iss_location import ISSLocation
from datetime import datetime, timedelta
from math import radians, sin, cos, atan2, sqrt

class WarehouseDataFormating:
    def __init__(self) -> None:
        self.connector = DatabaseConnector()
        self.iss_warehouse = ISSWarehouse()
        self.normalized_dataframe = None

    def clean_up_dataframe(self):
        self.normalized_dataframe.drop(["id", "altitude", "velocity", "footprint", "daynum",
                                        "solar_lat", "solar_lon"], inplace=True)

        # at the same time rearange columns
        self.normalized_dataframe = self.normalized_dataframe[["latitude", "longitude", "visibility", "date",
                                                               "current_location", "distance_travelled", "units"]]

    def get_starting_ending_points(self):
        # I had to substract 4 hours because of the time difference in time zones
        current_timestamp = (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
        five_minutes_ago = (datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        # print(current_timestamp,five_minutes_ago)
        starting_point, ending_point = self.iss_warehouse.select_data_in_range(five_minutes_ago, current_timestamp, self.connector)

        self.normalized_dataframe = ending_point
        return starting_point, ending_point

    def distance_calculation_formula(self, lat1, lon1, lat2, lon2):
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Calculate the differences between latitudes and longitudes
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # actual formula for distance calculation
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # convert it to kilometers and round to 4 decimal points
        distance = round(R * c, 4)

        return distance

    def calculate_travel_distance(self):
        starting_point, ending_point = self.get_starting_ending_points()
        lat1, lon1 = starting_point['latitude'], starting_point['longitude']
        lat2, lon2 = ending_point['latitude'],  ending_point['longitude']

        distance = self.distance_calculation_formula(lat1, lon1, lat2, lon2)
        self.normalized_dataframe["distance_travelled"] = distance

    def find_iss_location(self):
        iss_location = ISSLocation()
        location = iss_location.get_location(self.normalized_dataframe["latitude"], self.normalized_dataframe["longitude"])

        self.normalized_dataframe["current_location"] = location

def just_for_test():
    obj = WarehouseDataFormating()
    obj.get_starting_ending_points()
    obj.calculate_travel_distance()
    obj.find_iss_location()
    obj.clean_up_dataframe()
    return obj.normalized_dataframe

