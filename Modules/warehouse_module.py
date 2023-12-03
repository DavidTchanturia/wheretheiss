from Database.iss_wearhouse import ISSWarehouse
from Database.DBManager import DatabaseConnector, ISSDataWarehouseManager
from Constants.paths import PATH_TO_RAW_ISS_INFO_JSON
import time


def run_warehouse_module():
    """this module is responsible for extracting data from raw json file and loading it into warehouse"""
    db_connector = DatabaseConnector()

    # if warehouse table does not exist, create one
    data_warehouse_manager = ISSDataWarehouseManager(db_connector)
    data_warehouse_manager.create_table()

    obj = ISSWarehouse()

    while True:
        obj.select_data_from_json(PATH_TO_RAW_ISS_INFO_JSON)  # selects data that has not been inserted to warehouse
        obj.change_kilometer()  # change kilometers -> km
        obj.insert_to_warehouse(db_connector)  # insert into iss_24455_warehouse
        time.sleep(120)  # run every two minutes
