import os
# using this .py file to make all the paths in projects dynamic

# get the absolute path to pwd parent directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRECTORY = os.path.dirname(CURRENT_FILE_DIRECTORY)  # in this case wheretheiss

# add other inside paths to absolute path of wheretheiss
PATH_TO_RAW_ISS_INFO_JSON = os.path.join(PROJECT_DIRECTORY, 'RawData', 'raw_iss_info.json')
PATH_TO_DATABASE_VARIABLES_YAML = os.path.join(PROJECT_DIRECTORY, 'database_config.yaml')
LOGGER_FILE_LOG_PATH = os.path.join(PROJECT_DIRECTORY, 'Logger', 'iss.log')
