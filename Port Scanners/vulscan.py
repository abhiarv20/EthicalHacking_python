#!/usr/bin/python

import socket
#for checking ports
import os
#checks wheter the vul exsisit
import sys
#checks number of arg specified in command i.e. ./vulscan.py vulnbanners.txt

def retBanner(ip,port):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((ip,port))
		banner = s.recv(1024)
		return banner
	except:
		return
#checks the port is open or not


def checkVulns(banner, filename):
	f = open(filename, "r")
	#opening a file in python
	for line in f.readlines():
		if line.strip("\n") in banner:
			print '[+] Server is vulnerable: ' + banner.strip("\n")
#takes argument from the filename


def main():
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		#2 args i.e 0 and 1...for 0 python code..for 1 text file
		if not os.path.isfile(filename):
		#checks if file is present or not
			print '[-] File doesnot exsist!'
			exit(0)
		if not os.access(filename, os.R_OK):
		#checks if file permission is allowed to the user
			print '[-] Access denied'
			exit(0)
	else:
		print '[-] Usage: ' + str(sys.argv[0]) + " <vuln filename>"
		exit(0)

	portlist = [21,22,25,80,110,443,445]
	#list of port to scan
	for x in range(102,103):
		ip = "192.168.56." + str(x)
		for port in portlist:
			banner = retBanner(ip,port)
			if banner:
				print '[+]' + ip + "/" + str(port) + " : " + banner
				checkVulns(banner, filename)
	#runs the vulnerability scan
main()





