#!/usr/bin/env bash
echo "Setting streaming signal/silence thresholds on butt to 0 (disable)"
/usr/local/bin/butt-client -a 192.168.1.73 -M 0
sleep 1
/usr/local/bin/butt-client -a 192.168.1.73 -m 0
sleep 1
echo "Disconnecting any streams"
/usr/local/bin/butt-client -a 192.168.1.73 -d
sleep 1
