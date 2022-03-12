#!/usr/bin/env sh
# check file status of /tmp/healthz and return 0 if newer than 5 minutes
# return 1 if older than 5 minutes
set -xe
if [ -f /tmp/healthz ]; then
  if [ $(($(date +%s) - $(stat -c %Y /tmp/healthz))) -lt 300 ]; then
    exit 0
  else
    exit 1
  fi
else
  exit 1
fi
