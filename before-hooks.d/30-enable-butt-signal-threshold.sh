#!/usr/bin/env bash
echo "Setting streaming signal/silence thresholds on butt to a number (enable)"
/usr/local/bin/butt-client -a 192.168.1.73 -M 1
sleep 1
/usr/local/bin/butt-client -a 192.168.1.73 -m 60
