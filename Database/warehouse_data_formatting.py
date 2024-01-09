import pandas as pd
from Constants.variables import EARTH_RADIUS
from Database.DBManager import DatabaseConnector
from Database.iss_wearhouse import JsonToWarehouse
from GetData.get_iss_location import ISSLocation
from datetime import datetime, timedelta
from math import radians, sin, cos, atan2, sqrt
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class WarehouseDataFormatter:
    def __init__(self) -> None:
        self.connector = DatabaseConnector()
        self.iss_warehouse = JsonToWarehouse()
        self.normalized_dataframe = None

    def _clean_up_dataframe(self) -> None:
        """remove unnecessary rows from warehouse df, only leave ones for normalized table, rearange them"""
        try:
            # at the same time rearange columns
            self.normalized_dataframe = self.normalized_dataframe[["latitude", "longitude", "visibility", "date",
                                                                   "current_location", "distance_travelled"]]
        except Exception as exception:
            logger.error(f"exception occured: {exception}")

    def _get_starting_ending_points(self) -> tuple:
        """ starting point is the column with the min timestamp in the selected range
            ending point is the column with the max timestamp in the selected range"""
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        five_minutes_ago = (datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        # logger.log(f"==============================={current_timestamp}========={five_minutes_ago}")
        starting_point, ending_point = self.iss_warehouse.select_data_in_range(five_minutes_ago, current_timestamp, self.connector)

        self.normalized_dataframe = ending_point
        return starting_point, ending_point

    def _calculate_travel_distance(self) -> None:
        """get the starting, ending point, uses formula to calculate distance"""
        starting_point, ending_point = self._get_starting_ending_points()
        lat1, lon1 = starting_point['latitude'], starting_point['longitude']
        lat2, lon2 = ending_point['latitude'],  ending_point['longitude']

        distance = self._distance_calculation_formula(lat1, lon1, lat2, lon2)
        self.normalized_dataframe["distance_travelled"] = distance

    def _find_iss_location(self) -> None:
        """if iss is on top of a country, location will be a country name. if on top of water,
        location will be ocean name"""

        iss_location = ISSLocation()
        try:
            # retrieve based on lan and lon
            location = iss_location.get_location(self.normalized_dataframe["latitude"], self.normalized_dataframe["longitude"])
        except KeyError as key:
            logger.error(f'KeyError occured: {key}')
        finally:
            self.normalized_dataframe["current_location"] = location

    @staticmethod
    def _distance_calculation_formula( lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """general formula to calculate distance travelled using lan and lon"""
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Calculate the differences between latitudes and longitudes
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # actual formula for distance calculation
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # convert it to kilometers and round to 4 decimal points
        distance = round(EARTH_RADIUS * c, 4)

        return distance

    @staticmethod
    def wrapper_function() -> pd.DataFrame:
        obj = WarehouseDataFormatter()
        obj._get_starting_ending_points()
        obj._calculate_travel_distance()
        obj._find_iss_location()
        obj._clean_up_dataframe()
        return obj.normalized_dataframe