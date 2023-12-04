from RawData.save_raw_info import save_raw_iss_info
import time

def run_json_module():
    """this module is responsible for saving raw data into raw_iss_info.json

    sends request to api every 2 seconds. because every second times out"""
    while True:
        save_raw_iss_info()
        time.sleep(2)

run_json_module()
