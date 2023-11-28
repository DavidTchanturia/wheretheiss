import os

CURRENT_WORKING_DIRECTORY = os.getcwd()
PROJECT_DIRECTORY = os.path.dirname(CURRENT_WORKING_DIRECTORY)

PATH_TO_RAW_ISS_INFO_JSON = os.path.join(PROJECT_DIRECTORY, 'RawData', 'raw_iss_info.json')
