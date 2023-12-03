from Database.iss_normalized_database import ISSNormalizedDatabase
import time

def run_iss_insertion_module():
    """this module is responsible for extracting data from warehouse,
    transforming it and inserting into iss_normalized table"""

    # needs to be executed once outside of the loop
    normalized_data_for_insertion = ISSNormalizedDatabase()
    normalized_data_for_insertion.create_table_if_not_exists()  # if the iss_normalized table does not exist, create

    while True:
        normalized_data_for_insertion = ISSNormalizedDatabase()
        normalized_data_for_insertion.insert_into_normalized_table()  # insert normalized data


        time.sleep(300)  # will run every 5 minutes
