import json
import re
import datetime
import requests
from urllib.request import urlopen

today = datetime.datetime.today().weekday() % 5

mailgun_key_file = open("./secrets/mailgun-api-key.txt", "r")
mailgun_key = mailgun_key_file.read()

def send_simple_message(data):
    print("Sending: " + data)
    return requests.post(
        "https://api.mailgun.net/v3/cswift.tk/messages",
        auth=("api", mailgun_key),
        data={"from": "LunchBot <lunch@cswift.tk>",
              "to": ["Chandler Swift <3202964833@messaging.sprintpcs.com>",
                     "Eric Villnow <3205105180@vtext.com>"],
              "text": data})


with urlopen("http://gls.nutrislice.com/menu/glencoe-silver-lake-high/lunch/") as response:
    html_content = response.read()

encoding = response.headers.get_content_charset('utf-8')
html_text = html_content.decode(encoding)

a = re.search("bootstrapData\['menuMonthWeeks'\] = \[(.*?)\];", html_text)

data = json.loads(a.groups(0)[0])

try:
    todays_entree = data['days'][today]['menu_items'][1]['food']['name']
    side1 = data['days'][today]['menu_items'][2]['food']['name']
    side2 = data['days'][today]['menu_items'][3]['food']['name']
    if data['days'][today]['menu_items'][4]['food'] is not None:
        side3 = data['days'][today]['menu_items'][4]['food']['name']
    else:
        side3 = None
    message = "Today's Lunch is " + todays_entree + " with " + side1 + ", " + side2 + ((", " + side3) if side3 is not None else "")
    send_simple_message(message)
except:
    pass
