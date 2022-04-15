#!/usr/bin/env bash
function try_butt_command() {
  server_ip=$BUTT_SERVER_IP
  server_port=$BUTT_SERVER_PORT
  binary_path=/usr/local/bin/butt-client
  allowed_timeout=3s

  # We assume max number of args is 2, we can't use $@ to preserve quotings in args
  # we timeout the butt command after 3s, and print the total time taken
  # this is because the butt command is blocking if stuck, and we don't want to wait forever
  sleep 1
  time timeout $allowed_timeout $binary_path -a $server_ip -p $server_port "$1" "$2"
  # Note that both 'time' and 'timeout' functions transfer the exit code of the command <3
}
export -f try_butt_command

function butt_command() {
  max_attempts=10

  attempts=0
  while [ $attempts -lt $max_attempts ]; do
    try_butt_command "$1" "$2"
    if [ $? -ne 0 ]; then
      attempts=$((attempts+1))
      echo "Failed to send command to butt, retrying..."
    else
      return 0
    fi
  done
  echo "Failed to run butt command after $max_attempts attempts"
  exit 1
}

# the following export is important to make the function available to the callers sourcing this file
export -f butt_command
