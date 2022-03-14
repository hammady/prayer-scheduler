#!/usr/bin/env bash
echo "Setting streaming signal/silence thresholds on butt to 0 (disable)"
butt_command -M 0
butt_command -m 0
echo "Disconnecting any streams"
butt_command -d
