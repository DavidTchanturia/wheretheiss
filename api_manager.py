import requests
import json
from Constants.apis import WHERE_IS_ISS_SATELLITES_DETAILS, WHERE_IS_ISS_SATELLITES, REVERSE_GEOCODING_API


def get_satellite_id() -> int:
    response = requests.get(WHERE_IS_ISS_SATELLITES)
    response_json = response.json()
    satellite_id = response_json[0].get("id")

    return satellite_id


def get_satellite_details() -> json:
    satellite_id = get_satellite_id()
    url = WHERE_IS_ISS_SATELLITES_DETAILS.format(satellite_id=satellite_id)

    response = requests.get(url)
    response_json = response.json()

    return response_json


