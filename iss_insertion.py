from Database.iss_normalized_database import ISSNormalizedDatabase
import time


normalized_data_for_insertion = ISSNormalizedDatabase()
normalized_data_for_insertion.create_table_if_not_exists()  # if the iss_normalized table does not exist, create

while True:
    normalized_data_for_insertion = ISSNormalizedDatabase()
    normalized_data_for_insertion.insert_into_normalized_table()  # insert normalized data
    time.sleep(10)  # data is inserted every 10 sec, I did it so its easier to check the task. Normally to would be 5 min