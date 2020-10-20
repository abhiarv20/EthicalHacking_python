#!/usr/bin/python

import subprocess
#it allows you to execute system commands and checkout the outout they give inorder to see the macaddress
from termcolor import colored

def change_mac_address(interface,mac):

	subprocess.call(["ifconfig",interface,"down"])
	subprocess.call(["ifconfig",interface,"hw","ether",mac])
	subprocess.call(["ifconfig",interface,"up"])



def main():
	interface = str(input(colored("[*] Enter Interface To Change Mac Address on: ",'yellow')))
	#insert interface i.e. eth0, others
	new_mac_address = input(colored("[*] Enter Mac Address to change to: ",'blue'))

	before_change = subprocess.check_output(["ifconfig",interface])
	change_mac_address(interface,new_mac_address)
	after_change = subprocess.check_output(["ifconfig",interface])

	if before_change == after_change:
		print(colored("[!!] Failed to change MAC address to: " + new_mac_address,'red'))
	else:
		print(colored("[+] MAC address change to: " + new_mac_address + " on interface " + interface,'green'))

main()
