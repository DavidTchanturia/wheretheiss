import pandas as pd
import json
from api_manager import ISSSatelliteDetails
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON


def save_raw_iss_info() -> None:
    # Read existing data from the file or create an empty DataFrame
    try:
        with open(PATH_TO_RAW_ISS_INFO_JSON, 'r') as json_file:
            data = pd.read_json(json_file)
    except FileNotFoundError:
        data = pd.DataFrame()

    # Convert the new response to a DataFrame and append it to the existing data
    new_data = ISSSatelliteDetails().get_satellite_details()
    data = data._append(new_data, ignore_index=True)

    # Save the combined data to the JSON file
    data.to_json(PATH_TO_RAW_ISS_INFO_JSON, orient='records', indent=2)