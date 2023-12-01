from Constants.apis import REVERSE_GEOCODING_API
import requests


class ISSLocation:
    def __init__(self):
        self.api_url = REVERSE_GEOCODING_API  # this api uses lan and lon to give place name

    def get_location(self, latitude: float, longitude: float) -> str:
        api_url = self.api_url.format(latitude=latitude, longitude=longitude)
        response = requests.get(api_url).json()

        country = response.get("countryName")  # get the country name that the iss is above of
        if not country:
            # very often iss is on top of the ocean. so I get the ocean name if there is no country
            location = response.get("localityInfo")
            information = location.get("informative")[0]
            country = information.get("name")

        return country




