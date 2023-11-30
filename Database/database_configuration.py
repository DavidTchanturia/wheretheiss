import yaml
from Constants.paths import PATH_TO_DATABASE_VARIABLES_YAML


def parse_yaml(file_path=PATH_TO_DATABASE_VARIABLES_YAML):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        database_data = data["database"]

    return database_data
