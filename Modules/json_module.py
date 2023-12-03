from RawData.save_raw_info import save_raw_iss_info
import time


def run_json_module():
    while True:
        save_raw_iss_info()
        time.sleep(2)

