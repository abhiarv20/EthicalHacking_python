#!/usr/bin/python

import crypt
#imported crypt library which allows us to use salt passwords
from termcolor  import colored

def crackPass(cryptWord):
	salt = cryptWord[0:2]
	dictionary = open("dictionary.txt",'r')
	for word in dictionary.readlines():
		word = word.strip('\n')
		cryptPass = crypt.crypt(word, salt)
		if  (cryptWord == cryptPass):
			print(colored("[+] Found password: " + word,'green'))
			quit()
	print(colored("[-] Password not found",'red'))

0



def main():
	passFile = open('pass.txt','r')
	for line in passFile.readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptWord = line.split(':')[1].strip(' ').strip('\n')
			#print cryptWord
			print(colored("[*] Cracking Password For: " + user,'yellow'))
			crackPass(cryptWord)
main()
