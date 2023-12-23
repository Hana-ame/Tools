#!/bin/bash

OS=$(uname -s)
current_time=$(date +"%Y-%m-%d %H%M%S")

if [ "${OS}" = "Linux" ]; then  
#   echo "" > "chatGPT/${current_time}@${OS}.txt"
  vi "chatGPT/${current_time}@${OS}.txt"
elif [ "${OS}" = "Darwin" ]; then
  echo "Current system is macOS"
elif [ "${OS}" = "FreeBSD" ]; then
  echo "Current system is FreeBSD"
else
  echo "Unknown system"
  echo "" > "chatGPT/${current_time}@${OS}.txt"
  notepad "chatGPT/${current_time}@${OS}.txt"
fi
