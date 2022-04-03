#!/usr/bin/env bash

# start the cron service
service cron start

# run the command
$@

if [ $? -ne 0 ]; then
  echo "Command failed"
  exit 1
fi

echo "Watching log file..."
f=/var/log/app.log
touch $f && chmod a+w $f && tail -f $f
