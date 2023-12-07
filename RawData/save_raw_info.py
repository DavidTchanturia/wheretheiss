import pandas as pd
from api_manager import ISSSatelliteDetails
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON


def save_raw_iss_info() -> None:
    # create pandas dataframe of existing data in json file
    try:
        with open(PATH_TO_RAW_ISS_INFO_JSON, 'r') as json_file:
            # convert_date needs to be False, otherwise pandas will convert it automatically
            data = pd.read_json(json_file, convert_dates=False)
    except FileNotFoundError:
        data = pd.DataFrame()  # create empty dataframe if there is no info in json

    # add new response to existing one
    new_data = ISSSatelliteDetails().get_satellite_details()
    frames_to_concat = [data, new_data]
    data = pd.concat(frames_to_concat)  # use pandas concat instead of _append

    # add new data to json
    data.to_json(PATH_TO_RAW_ISS_INFO_JSON, orient='records', indent=2)