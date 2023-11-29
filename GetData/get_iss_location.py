import pandas as pd
from Constants.apis import REVERSE_GEOCODING_API
from api_manager import ISSSatelliteDetails
import requests

class ISSLocation:
    def __init__(self, api_url=REVERSE_GEOCODING_API):
        self.api_url = api_url

    def get_location(self, latitudes, longitudes) -> pd.Series:
        api_url_list = [self.api_url.format(latitude=lat, longitude=lon) for lat, lon in zip(latitudes, longitudes)]

        responses = [requests.get(url).json() for url in api_url_list]

        countries = []
        for response in responses:
            country = response.get("countryName")
            if not country:
                location = response.get("localityInfo")
                information = location.get("informative")[0]
                country = information.get("name")
            countries.append(country)

        return pd.Series(countries)



