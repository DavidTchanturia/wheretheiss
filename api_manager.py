import requests
import pandas as pd
from Constants.apis import WHERE_IS_ISS_SATELLITES_DETAILS, WHERE_IS_ISS_SATELLITES, REVERSE_GEOCODING_API

class ISSSatelliteDetails:
    def __init__(self):
        self.satellite_id = self.get_satellite_id()
        self.details_df = None

    def get_satellite_id(self) -> int:
        response = requests.get(WHERE_IS_ISS_SATELLITES)
        response_json = response.json()
        self.satellite_id = response_json[0].get("id")
        return self.satellite_id

    def get_satellite_details(self) -> pd.DataFrame:
        if not self.satellite_id:
            self.get_satellite_id()

        url = WHERE_IS_ISS_SATELLITES_DETAILS.format(satellite_id=self.satellite_id)
        response = requests.get(url)
        response_json = response.json()

        # Use pandas to create a DataFrame from the JSON response
        self.details_df = pd.json_normalize(response_json)

        return self.details_df
