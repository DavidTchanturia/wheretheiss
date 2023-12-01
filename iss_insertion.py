from Database.iss_normalized_database import ISSNormalizedDatabase
import time

# needs to be executed once outside of the loop
normalized_data_for_insertion = ISSNormalizedDatabase()
normalized_data_for_insertion.create_table_if_not_exists()  # if the iss_normalized table does not exist, create

while True:
    normalized_data_for_insertion = ISSNormalizedDatabase()
    normalized_data_for_insertion.insert_into_normalized_table()  # insert normalized data

    # modify as you see fit
    time.sleep(5)  # data is inserted every 10 sec, however insertion is done using 5 minute chunks of table
