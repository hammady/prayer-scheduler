#!/usr/bin/env bash
if [ $# -ne 2 ]; then
  echo "USAGE: $0 <before|after> <prayer-name>"
  exit 1
fi

if [ "$1" != "before" ] && [ "$1" != "after" ]; then
  echo "First argument should be either 'before' or 'after'"
  exit 1
fi

before_after="$1"
prayer_name="$2"
root_dir=`dirname $0`

# Run hooks
for hook in $root_dir/${before_after}-hooks.d/*; do
    echo "Running ${before_after} hook: $hook"
    $hook $prayer_name
done
