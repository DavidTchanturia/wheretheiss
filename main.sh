#!/bin/bash

# Set the project root directory
PROJECT_ROOT=$(dirname "$(readlink -f "$0")")

# when ctrl + c pressed, both will stop
cleanup() {
    echo "Stopping scripts..."
    pkill -P $$
    exit 0
}

trap cleanup INT

# include project path to avoid import errors
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# start json module, which saves raw data
echo "Starting json_module.py"
python3 "$PROJECT_ROOT/Modules/json_module.py" &

# wait for 120 seconds and start warehouse_module.py, which saves data from raw to warehouse
sleep 30
echo "Starting warehouse_module.py"
python3 "$PROJECT_ROOT/Modules/warehouse_module.py" &

# In total, wait for 300 seconds and start iss_insertion_module.py
# this module extracts, transforms adds some addition info and inserts into iss_normalized table
sleep 60
echo "Starting iss_insertion_module.py"
python3 "$PROJECT_ROOT/Modules/iss_insertion_module.py" &
wait
