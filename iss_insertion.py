from Database.iss_normalized_database import ISSNormalizedDatabase
import time


normalized_data_for_insertion = ISSNormalizedDatabase()
normalized_data_for_insertion.create_table_if_not_exists()

while True:
    normalized_data_for_insertion = ISSNormalizedDatabase()
    normalized_data_for_insertion.insert_into_normalized_table()
    time.sleep(10)