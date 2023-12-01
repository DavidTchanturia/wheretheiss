from RawData.save_raw_info import ISSSatelliteDetails
from Database.iss_wearhouse import ISSWarehouse
from Database.DBManager import DatabaseConnector, ISSDataWarehouseManager
from RawData.save_raw_info import save_raw_iss_info
import time

db_connector = DatabaseConnector()

# if warehouse table does not exist, create one
data_warehouse_manager = ISSDataWarehouseManager(db_connector)
data_warehouse_manager.create_table()


def main():

    # initialize object to get details later
    dataframe = ISSSatelliteDetails()
    save_raw_iss_info()  # save the raw info in json file
    dataframe = dataframe.get_satellite_details()  # get iss details from wheretheiss api as pd dataframe

    # modify data to be inserted in warehouse
    warehouse_dataframe = ISSWarehouse(dataframe)
    warehouse_dataframe.convert_timestamp_to_datetime()  # timestamp -> datetime
    warehouse_dataframe.change_kilometer()  # changes kilometers -> km

    # Insert data into the warehouse
    warehouse_dataframe.insert_to_warehouse(db_connector)  # insert all the data



if __name__ == '__main__':
    while True:
        main()
        time.sleep(2)

