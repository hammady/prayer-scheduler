#!/usr/bin/env bash

# set timezone
if [ ! -z "$CRON_TIMEZONE" ]; then
  ln -sf /usr/share/zoneinfo/$CRON_TIMEZONE /etc/localtime
fi

# start the cron service
service cron start

# capture environment variables for cronjobs
env >> /home/$CRON_USER/.env

# run the command
$@

if [ $? -ne 0 ]; then
  echo "Command failed"
  exit 1
fi

echo "Watching log file..."
f=/var/log/app.log
touch $f && chmod a+w $f && tail -f $f
