import pandas as pd
import json
from api_manager import get_satellite_details
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON


def save_raw_iss_info(iss_info: json) -> None:
    # Read existing data from the file
    try:
        with open(PATH_TO_RAW_ISS_INFO_JSON, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    # Append the new response to the existing data
    data.append(iss_info)

    with open(PATH_TO_RAW_ISS_INFO_JSON, 'w') as json_file:
        json.dump(data, json_file, indent=2)

