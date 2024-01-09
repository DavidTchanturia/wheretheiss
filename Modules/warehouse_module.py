from Database.iss_wearhouse import JsonToWarehouse
from Database.DBManager import DatabaseConnector
import time


def run_warehouse_module():
    """this module is responsible for extracting data from raw json file and loading it into warehouse"""
    db_connector = DatabaseConnector()
    obj = JsonToWarehouse()
    obj.create_iss_warehouse_table(db_connector)

    while True:
        obj.get_warehouse_data_wrapper(db_connector)
        time.sleep(30)  # run every two minutes


# set this up for bash script to run the function
run_warehouse_module()
