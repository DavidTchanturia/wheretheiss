from Database.iss_normalized_database import WarehouseToIssTable
import time

def run_iss_insertion_module():
    """this module is responsible for extracting data from warehouse,
    transforming it and inserting into iss_normalized table"""
    normalized_data_for_insertion = WarehouseToIssTable()
    normalized_data_for_insertion.create_table_if_not_exists()

    while True:
        normalized_data_for_insertion = WarehouseToIssTable()
        normalized_data_for_insertion.insert_into_normalized_table()  # insert normalized data

        time.sleep(60)  # will run every 5 minutes


# set this up for bash script to run the function
run_iss_insertion_module()
