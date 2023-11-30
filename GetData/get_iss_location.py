import pandas as pd
from Constants.apis import REVERSE_GEOCODING_API
from api_manager import ISSSatelliteDetails
import requests

class ISSLocation:
    def __init__(self):
        self.api_url = REVERSE_GEOCODING_API

    def get_location(self, latitude, longitude) -> str:
        api_url = self.api_url.format(latitude=latitude, longitude=longitude)
        response = requests.get(api_url).json()

        country = response.get("countryName")
        if not country:
            location = response.get("localityInfo")
            information = location.get("informative")[0]
            country = information.get("name")

        return country




