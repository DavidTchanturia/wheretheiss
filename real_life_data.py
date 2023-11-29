from RawData.save_raw_info import ISSSatelliteDetails
from Database.iss_wearhouse import ISSWarehouse
from Database.DBManager import DatabaseConnector, ISSDataWarehouseManager
from RawData.save_raw_info import save_raw_iss_info
import time


def warehouse_seeder():
    # Create a DatabaseConnector instance
    db_connector = DatabaseConnector()

    # if it does not exist create table
    data_warehouse_manager = ISSDataWarehouseManager(db_connector)
    data_warehouse_manager.create_table()

    # get the iss details
    dataframe = ISSSatelliteDetails()
    save_raw_iss_info() # save raw details
    dataframe = dataframe.get_satellite_details()

    # modify data to be inserted in warehouse
    warehouse_dataframe = ISSWarehouse(dataframe)
    warehouse_dataframe.convert_timestamp_to_datetime()
    warehouse_dataframe.change_kilometer()

    # Insert data into the warehouse
    warehouse_dataframe.insert_to_warehouse(db_connector)

    db_connector.close_connection()



while True:
    warehouse_seeder()
    time.sleep(1)