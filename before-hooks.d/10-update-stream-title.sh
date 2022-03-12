#!/usr/bin/env bash
prayer_name="$1"

echo "Setting stream title for prayer: $prayer_name"

function butt_command() {
  /usr/local/bin/butt-client -a 192.168.1.73 -u "$1"
}

case $prayer_name in
  fajr)
    butt_command "Masjid Live - Fajr Athan and Prayer"
    ;;
  dhuhr)
    butt_command "Masjid Live - Dhuhr Athan and Prayer"
    ;;
  asr)
    butt_command "Masjid Live - Asr Athan and Prayer"
    ;;
  maghrib)
    butt_command "Masjid Live - Maghrib Athan and Prayer"
    ;;
  isha)
    butt_command "Masjid Live - Isha Athan and Prayer"
    ;;
  jumaa1)
    butt_command "Masjid Live - Jumaa 1st Athan, Khutba and Prayer"
    ;;
  jumaa2)
    butt_command "Masjid Live - Jumaa 2nd Athan, Khutba and Prayer"
    ;;
  jumaa3)
    butt_command "Masjid Live - Jumaa 3rd Athan, Khutba and Prayer"
    ;;
  jumaa4)
    butt_command "Masjid Live - Jumaa 4th Athan, Khutba and Prayer"
    ;;
  jumaa5)
    butt_command "Masjid Live - Jumaa 5th Athan, Khutba and Prayer"
    ;;
  *)
    butt_command "Masjid Live - General"
    ;;
esac
