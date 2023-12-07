import yaml
from Constants.paths import PATH_TO_DATABASE_VARIABLES_YAML
from Logger.iss_logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


# simply parse yaml to get database configuration details
def parse_yaml(file_path=PATH_TO_DATABASE_VARIABLES_YAML):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            database_data = data["database"]
        return database_data
    except FileNotFoundError as error:
        logger.error(f"file can not be found on the path specified: {error}")
    except yaml.YAMLError as error:
        logger.error(f"yaml error: {error}")
