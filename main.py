import threading
import time
from Modules.json_module import run_json_module
from Modules.warehouse_module import run_warehouse_module
from Modules.iss_insertion_module import run_iss_insertion_module

"""main.py will be creating three main threads for three parts of the program
run_json_module -> saves raw data in json file

run_warehouse_module -> starts running after 2 minutes and saves data to warehouse from raw json
every two minutes

run_iss_insertion_module -> starts running after 5 minutes and saves data from warehouse to
iss_normalized table where some calculation and changes have been made

threads will run independently of each other. only once will they wait for each other to start running
in the beginning"""

def main():
    # Sstart json thread
    json_thread = threading.Thread(target=run_json_module)
    json_thread.start()

    # warehouse thread after 2 minutes
    time.sleep(120)
    warehouse_thread = threading.Thread(target=run_warehouse_module)
    warehouse_thread.start()

    # iss_normalized thread after 5 minutes of json thread
    time.sleep(180)  # 180 + 120 = 300
    iss_table_thread = threading.Thread(target=run_iss_insertion_module)
    iss_table_thread.start()


if __name__ == "__main__":
    main()