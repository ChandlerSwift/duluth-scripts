# Scripts
0;115;0c
These scripts are used on my (sometimes Raspberry Pi-hosted) Duluth server
for task automation and other sometimes-cool uses.

###`newspaper_download.sh`
On Wednesdays, the McLeod County Chronicle is released online.
This script downloads the newspaper, and emails it out to a handful
of people who have requested to be added to my mailing list.
(TODO: actual mailing list)
```
# Download/Email newspaper, 2p Wed
0 14 * * Wed  /home/chandler/scripts/newspaper_download.sh
```

###`get_data_usage.sh`
For use with the [analog meter](http://experiments.chandlerswift.com/analog-meter/).
Gets data from https://billing.broadband-mn.com/datausage.php.
I use a cronjob to run this hourly:
```
# Update analog meter with Broadband MN Data Usage
0 * * * * /bin/bash /home/chandler/scripts/get_data_usage.sh -b > /var/www/experiments/analog-meter/get-value
```
