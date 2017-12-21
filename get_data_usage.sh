#!/bin/bash
# get_data_usage.sh
# Gets data usage in GB from broadband-mn account
# OPTIONS:
#   -b     # Prints data usage

tmpfile=$(mktemp)

# obtain cookie
curl --silent --cookie-jar $tmpfile "https://billing.broadband-mn.com/index.php" \
     --data "username=dswift&password=$(cat $(dirname $0)/secrets/broadband_password.txt)" > /dev/null

#echo -----------------------------------
#echo COOKIE INFORMATION\:
#cat $tmpfile
#echo -----------------------------------

gbs_used=`curl --silent --cookie $tmpfile "https://billing.broadband-mn.com/datausage.php"\
| grep -o "Total Usage: [0-9]*" | grep -o '[0-9]*'`

rm $tmpfile

if [ "$1" == "-b" ]; then # for Bit or Binary or something?
    if [ $gbs_used -gt 255 ]; then gbs_used=255; fi # overflow protection
    echo $(( "$gbs_used" * 255 / 100))
else
    echo $gbs_used
fi
