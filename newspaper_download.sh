#!/bin/bash

month=$(/bin/date +%-m)
day=$(/bin/date +%-d)
year=$(/bin/date +%-Y)

cd /var/www/duluth/newspapers/$year

until wget -N http://www.glencoenews.com/sites/default/files/A-Section%20${month}-$day.pdf
do
  sleep 10m
done

until wget -N http://www.glencoenews.com/sites/default/files/B-Section%20${month}-$day.pdf
do
  sleep 10m
done

echo curl --user "$(cat $(dirname $0)/secrets/mailgun-api-key.txt)" \
    https://api.mailgun.net/v3/cswift.tk/messages \
    -F from='NewsBot <news@cswift.tk>' \
    -F to=chandler@chandlerswift.com \
    -F to=villnoweric@gmail.com \
    -F to=celine@swiftgang.net \
    -F to=jacobwawrzyniak@gmail.com \
    -F to=res@swiftgang.net \
    -F subject='McLeod County Chronicle: '$month/$day \
    -F text="New newspapers available!
A section: http://duluth.chandlerswift.com/newspapers/${year}/A-Section%20${month}-${day}.pdf
B section: http://duluth.chandlerswift.com/newspapers/${year}/B-Section%20${month}-${day}.pdf
Archives:  http://duluth.chandlerswift.com/newspapers/" \
    -F html="
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml'>
 <head>
  <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
  <title>McLeod County Chronicle: ${month}/${day}</title>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
</head>
<body style='margin: 0; padding: 0;'>
  <p style='color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;'>
    New Newspaper! Here are the links:
  </p>
  <a href='http://duluth.chandlerswift.com/newspapers/${year}/A-Section%20${month}-$day.pdf'>A Section</a>, <a href='http://duluth.chandlerswift.com/newspapers/${year}/B-Section%20${month}-$day.pdf'>B Section</a>
  <br /><br />
  <p style='color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;'>
    Archives: <a href='https://duluth.chandlerswift.com/newspapers/'>duluth.chandlerswift.com/newspapers/</a>
  </p>
</body>
</html>
"
