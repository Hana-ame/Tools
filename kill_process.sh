#!/bin/bash
# usage: bash kill_process.sh [port_number]

# Define the port number you want to search for
# PORT_NUMBER="$1"

# Find the PID of the process using the specified port
PID=$(lsof -t -i @[2001:470:c:6c::3]:22)

if [ -z "$PID" ]; then
  echo "No process found listening on port $PORT_NUMBER."
else
  # Terminate the process using the port
  kill $PID
  echo "Process with PID $PID has been terminated."
fi

