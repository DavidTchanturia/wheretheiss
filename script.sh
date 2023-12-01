#!/bin/bash

# when ctrl + c pressed, both will stop
cleanup() {
    echo "Stopping scripts..."
    pkill -P $$
    exit 0
}


trap cleanup INT

# first install all the requirements from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt


# first main.py will start runnning
echo "Running main.py..."
python3 /home/user/Sweeft/Projects/wheretheiss/main.py &

# Sleep for 5 minutes, but in this case to make it faster I'll do 10 seconds
# best case would be to start this after five minutes
sleep 10

# Run iss_insertion.py in the background
echo "Running iss_insertion.py..."
python3 /home/user/Sweeft/Projects/wheretheiss/iss_insertion.py &


wait
