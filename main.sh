#!/bin/bash

# when ctrl + c pressed, both will stop
cleanup() {
    echo "Stopping scripts..."
    pkill -P $$
    exit 0
}

trap cleanup INT

# include project path to avoid import errors
export PYTHONPATH=$PYTHONPATH:/home/user/Sweeft/Projects/wheretheiss

# install requirements
echo "Installing dependencies..."
pip install -r /home/user/Sweeft/Projects/wheretheiss/requirements.txt

# start json module, which saves raw data
echo "Starting json_module.py"
python3 /home/user/Sweeft/Projects/wheretheiss/Modules/json_module.py &

sleep 120 # wait for 120 seconds and start warehouse_module.py
echo "Starting warehouse_module.py"
python3 /home/user/Sweeft/Projects/wheretheiss/Modules/warehouse_module.py &

# In total, wait for 300 seconds and start iss_insertion_module.py
sleep 180
echo "Starting iss_insertion_module.py"
python3 /home/user/Sweeft/Projects/wheretheiss/Modules/iss_insertion_module.py &
wait
