import pandas as pd
from api_manager import ISSSatelliteDetails
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON


def save_raw_iss_info() -> None:
    # create pandas dataframe of existing data in json file
    try:
        with open(PATH_TO_RAW_ISS_INFO_JSON, 'r') as json_file:
            data = pd.read_json(json_file)
    except FileNotFoundError:
        data = pd.DataFrame() # create empty dataframe if there is no info in json

    # add new response to existing one
    new_data = ISSSatelliteDetails().get_satellite_details()
    data = data._append(new_data, ignore_index=True)  # just append did not work, using _append because of that

    # add new data to json
    data.to_json(PATH_TO_RAW_ISS_INFO_JSON, orient='records', indent=2)