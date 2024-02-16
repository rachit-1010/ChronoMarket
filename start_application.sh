#!/bin/bash
# Bash script to start Flask microservices locally and gracefully stop them with a single Ctrl + C

declare -a pids=()

# Function to start a Flask microservice
start_flask() {
  python3 "$1" &
  pids+=($!)
}

# Start accounts microservice
start_flask "microservices/accounts/accounts.py"

# Start bid microservice
start_flask "microservices/bidding/bidding.py"

# start items microservice
start_flask "microservices/items/item_microservice.py"

# start auction microservice
start_flask "microservices/auction_platform/auctions.py"

# start notifications microservice
start_flask "microservices/notifications/notifications.py"

# start items microservice
start_flask "microservices/auction_platform/auto_change_auction_status.py"

# Function to stop the servers
stop_servers() {
  echo "Stopping servers..."
  for pid in "${pids[@]}"; do
    echo "Terminating process with PID: $pid"
    kill -TERM "$pid"
  done
  sleep 2 # Allow time for graceful shutdown
  exit
}

# Trap termination signal to stop the servers
trap 'stop_servers' SIGINT

echo "Servers started. Press Ctrl + C to stop."
# Add any additional setup or logging if needed
# ...

# Keep the script running
while true; do
  sleep 1
done