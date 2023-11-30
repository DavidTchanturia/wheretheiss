import logging
from Constants.paths import LOGGER_FILE_LOG_PATH

# simple logger config
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOGGER_FILE_LOG_PATH),
            logging.StreamHandler()
        ]
    )
