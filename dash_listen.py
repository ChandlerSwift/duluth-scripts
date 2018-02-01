import socket
import struct
import binascii
import time
import json
import urllib2
import base64

macs = {
    '40b4cda7323d': {'name': "Dash Button 1 (AmazonBasics Batteries)", 'id': 1}
}
username = "chandler@chandlerswift.com"
password = "swift24"

def call_light(url):
    request = urllib2.Request('https://duluth.chandlerswift.com/light/' + url)
    base64string = base64.b64encode('%s:%s' % (username, password))
    request.add_header("Authorization", "Basic %s" % base64string)   
    response = urllib2.urlopen(request)
    return response.read()

def toggle_light():
    jsonstr = json.loads(call_light('lights'))
    if jsonstr[1]["status"] is 0 and jsonstr[2]["status"] is 0 and jsonstr[3]["status"] is 0:
        query_str = "?1=255&2=255&3=255"
    else:
        query_str = "?1=0&2=0&3=0"
    call_light('light/set' + query_str)

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue
    # read out data
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if source_mac in macs:
        print "ARP from " + macs[source_mac]['name'] + " (MAC " + source_mac + ") with IP " + source_ip
        if macs[source_mac]['id'] == 1:
            toggle_light()
        if macs[source_mac]['id'] == 2:
            pass
    else:
        print "Unknown MAC " + source_mac + " from IP " + source_ip
