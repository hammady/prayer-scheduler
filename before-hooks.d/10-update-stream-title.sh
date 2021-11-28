#!/usr/bin/env bash
prayer_name="$1"

echo "Setting stream title for prayer: $prayer_name"

function replace_file_contents() {
    (
    if [ -z "$1" ]; then
        echo
    else
        echo "$1"
    fi
    ) > /stream-config/stream-title.txt
}

case $prayer_name in
  fajr)
    replace_file_contents "Masjid Live - Fajr Athan and Prayer"
    ;;
  dhuhr)
    replace_file_contents "Masjid Live - Dhuhr Athan and Prayer"
    ;;
  asr)
    replace_file_contents "Masjid Live - Asr Athan and Prayer"
    ;;
  maghrib)
    replace_file_contents "Masjid Live - Maghrib Athan and Prayer"
    ;;
  isha)
    replace_file_contents "Masjid Live - Isha Athan and Prayer"
    ;;
  jumaa1)
    replace_file_contents "Masjid Live - Jumaa 1st Athan, Khutba and Prayer, next at 1:15"
    ;;
  jumaa2)
    replace_file_contents "Masjid Live - Jumaa 2nd Athan, Khutba and Prayer, next at 2:00"
    ;;
  jumaa3)
    replace_file_contents "Masjid Live - Jumaa 3rd and Final Athan, Khutba and Prayer"
    ;;
  *)
    replace_file_contents "Masjid Live - General"
    ;;
esac
