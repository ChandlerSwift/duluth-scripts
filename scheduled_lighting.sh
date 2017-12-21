#!/bin/bash
# This script is used by cron to set lights according to a set schedule.

WGET="wget -qO - --user chandler@chandlerswift.com --password \"$(cat $(dirname $0)/secrets/light-pass.txt)\""
BASE_URL="https://duluth.chandlerswift.com/light/light"

case $1 in
    630am)
        # Monday through Friday at 6:30 AM, turn on light
        $WGET $BASE_URL"/set?0=1&scheduled=630am" > /dev/null
        ;;
    945pm)
        # Sunday through Thursday at 9:45, turn off main light and turn on red LEDs if main light is on
        [ "$($WGET $BASE_URL"/status?id=0&scheduled=945pmquery")" != 0 ] && $WGET $BASE_URL"/set?0=0&1=255&2=0&3=0&scheduled=945pmred" > /dev/null
        ;;
    10pm)
        # Sunday through Thursday at 10:00, dim red LEDs if on at 100%
        [ "$($WGET $BASE_URL"/status?id=1&scheduled=10pmquery")" == 255 ] && $WGET $BASE_URL"/set?1=50&2=0&3=0&scheduled=10pmdim" > /dev/null
        ;;
esac
