import time
from ssl import SSLError
import requests
import pandas as pd
from Constants.apis import WHERE_IS_ISS_SATELLITES_DETAILS, WHERE_IS_ISS_SATELLITES, REVERSE_GEOCODING_API
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class ISSSatelliteDetails:
    def __init__(self):
        self.satellite_id = self.get_satellite_id()
        self.details_df = None

    def get_satellite_id(self) -> int:
        try:
            response = requests.get(WHERE_IS_ISS_SATELLITES)
            response_json = response.json()

            self.satellite_id = response_json[0].get("id")
            return self.satellite_id
        except SSLError:
            time.sleep(2)
            return self.get_satellite_id()


    def get_satellite_details(self) -> pd.DataFrame:
        try:
            if not self.satellite_id:
                self.get_satellite_id()

            url = WHERE_IS_ISS_SATELLITES_DETAILS.format(satellite_id=self.satellite_id)
            response = requests.get(url)

            response_json = response.json()

            # create a dataframe form json
            self.details_df = pd.json_normalize(response_json)
            return self.details_df
        except SSLError:
            time.sleep(2)
            return self.get_satellite_details()