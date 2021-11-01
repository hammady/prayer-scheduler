#!/usr/bin/env bash

# start the cron service
service cron start

# run the command
$@

if [ $? -ne 0 ]; then
  echo "Command failed"
  exit 1
fi

echo "Sleeping forever to allow cron to run..."
sleep infinity