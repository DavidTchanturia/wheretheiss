import os

CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRECTORY = os.path.dirname(CURRENT_FILE_DIRECTORY)

PATH_TO_RAW_ISS_INFO_JSON = os.path.join(PROJECT_DIRECTORY, 'RawData', 'raw_iss_info.json')
