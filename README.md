# Scripts
These scripts are used on my (sometimes Raspberry Pi-hosted) Duluth server
for task automation and other sometimes-cool uses.

### `newspaper_download.sh`
On Wednesdays, the McLeod County Chronicle is released online.
This script downloads the newspaper, and emails it out to a handful
of people who have requested to be added to my mailing list.
(TODO: actual mailing list)
```
# Download/Email newspaper, 2p Wed
0 14 * * Wed  /home/chandler/scripts/newspaper_download.sh
```

### `get_data_usage.sh`
For use with the [analog meter](https://experiments.chandlerswift.com/analog-meter/).
Gets data from https://billing.broadband-mn.com/datausage.php.
I use a cronjob to run this hourly:
```
# Update analog meter with Broadband MN Data Usage
0 * * * * /bin/bash /home/chandler/scripts/get_data_usage.sh -b > /var/www/experiments/analog-meter/get-value
```

### `scheduled_lighting.sh`
Cron calls this to set the lights at scheduled times of day. Previously these
scripts lived in my crontab, but that just got too unwieldy.

```
# Monday through Friday at 6:30 AM, turn on light
30 6 * * 1-5 /home/chandler/scripts/scheduled_lighting.sh 630am

# Sunday through Thursday at 9:45, turn off main light and turn on red LEDs if main light is on
45 21 * * 0-4 /home/chandler/scripts/scheduled_lighting.sh 945pm

# Sunday through Thursday at 10:00, dim red LEDs if on at 100%
0 22 * * 0-4 /home/chandler/scripts/scheduled_lighting.sh 10pm
```

### `update_dns.sh`
```
# Dynamic DNS, updated every 5 minutes
0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/chandler/scripts/dns_update.sh
```
